import os
import sys
import json
import threading
import time
from pathlib import Path
from typing import Optional, List
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import uvicorn

from .rag_system import LocalRAGSystem
from .utils import convert_windows_path_to_wsl, validate_project_path
from .file_watcher import FileWatcherManager
from .file_watcher import FileWatcherManager

# Configuration
class Settings(BaseSettings):
    project_path: str = "/mnt/c/Users/Default/Projects"
    log_level: str = "INFO"
    max_context_tokens: int = 4000
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    vector_db_path: str = "/app/data/chroma_db"
    redis_url: Optional[str] = None
    file_watcher_enabled: bool = True
    file_watcher_debounce_seconds: float = 2.0
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/rag_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Multi-project support: Dictionary of project_path -> RAGSystem
rag_systems: dict[str, LocalRAGSystem] = {}
current_project: Optional[str] = None

file_watcher_manager = FileWatcherManager()
watcher_thread_stop = threading.Event()
watcher_thread: Optional[threading.Thread] = None

def load_existing_projects():
    """Load previously indexed projects on startup"""
    global rag_systems, current_project
    
    logger.info("Loading existing indexed projects...")
    chroma_db_path = Path(settings.vector_db_path)
    
    if not chroma_db_path.exists():
        logger.info("No existing ChromaDB found")
        return
    
    # Find all metadata files
    metadata_files = list(chroma_db_path.glob("metadata_*.json"))
    logger.info(f"Found {len(metadata_files)} metadata files")
    
    for metadata_file in metadata_files:
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                project_root = metadata.get("project_root")
                
                if not project_root:
                    continue
                
                project_path = Path(project_root)
                if not project_path.exists():
                    logger.warning(f"Project path no longer exists: {project_root}")
                    continue
                
                # Create RAG system for this project
                logger.info(f"Loading project: {project_root}")
                rag_system = LocalRAGSystem(
                    project_root=project_root,
                    vector_db_path=settings.vector_db_path,
                    embedding_model=settings.embedding_model,
                    redis_url=settings.redis_url,
                    max_context_tokens=settings.max_context_tokens
                )
                
                rag_systems[project_root] = rag_system
                
                # Set as current if it's the first one
                if current_project is None:
                    current_project = project_root
                
                logger.info(f"✅ Loaded project: {project_root} ({len(rag_system._indexed_files)} files)")
                
        except Exception as e:
            logger.error(f"Error loading project from {metadata_file}: {e}", exc_info=True)
    
    if rag_systems:
        logger.info(f"Successfully loaded {len(rag_systems)} projects")
    else:
        logger.info("No projects were loaded")

def file_watcher_background_task():
    """Background task to process pending file changes"""
    logger.info("File watcher background task started")
    while not watcher_thread_stop.is_set():
        try:
            file_watcher_manager.process_all_pending_changes()
        except Exception as e:
            logger.error(f"Error in file watcher background task: {e}", exc_info=True)
        time.sleep(1)  # Check every second
    logger.info("File watcher background task stopped")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global watcher_thread
    logger.info("🚀 Starting RAG Server...")
    
    # Load existing indexed projects
    load_existing_projects()
    
    # Start file watcher background task
    watcher_thread = threading.Thread(target=file_watcher_background_task, daemon=True)
    watcher_thread.start()
    logger.info("File watcher background task thread started")
    
    yield
    
    logger.info("Shutting down RAG Server...")
    watcher_thread_stop.set()
    if watcher_thread:
        watcher_thread.join(timeout=5)
    file_watcher_manager.stop_all()

app = FastAPI(
    title="Local RAG Server for GitHub Copilot",
    description="Optimizes context for GitHub Copilot using RAG",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class IndexRequest(BaseModel):
    project_path: str = Field(..., description="Project path (Windows or WSL)")
    file_extensions: Optional[List[str]] = Field(default=[".py", ".js", ".ts", ".java", ".cs", ".cpp", ".h", ".go", ".rs", ".jsx", ".tsx", ".vue"])
    force_reindex: bool = Field(default=False)

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    max_results: int = Field(default=5, ge=1, le=20)
    include_metadata: bool = Field(default=True)
    project_path: Optional[str] = Field(default=None, description="Specific project to query (optional, uses current if not specified)")

class SwitchRequest(BaseModel):
    project_path: str = Field(..., description="Project path to switch to (Windows or WSL)")

class QueryResponse(BaseModel):
    optimized_prompt: str
    context_chunks: int
    token_count: int
    metadata: Optional[dict] = None

# Endpoints
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "indexed_projects": len(rag_systems),
        "current_project": current_project,
        "projects": list(rag_systems.keys()),
        "vector_db_status": "healthy" if Path(settings.vector_db_path).exists() else "not_initialized"
    }

@app.post("/index")
async def index_project(request: IndexRequest, background_tasks: BackgroundTasks):
    global rag_systems, current_project
    
    try:
        wsl_path = convert_windows_path_to_wsl(request.project_path)
        logger.info(f"Indexing project: {wsl_path}")
        
        if not validate_project_path(wsl_path):
            raise HTTPException(status_code=400, detail=f"Invalid path: {wsl_path}")
        
        # Create or update RAG system for this project
        rag_system = LocalRAGSystem(
            project_root=wsl_path,
            vector_db_path=settings.vector_db_path,
            embedding_model=settings.embedding_model,
            redis_url=settings.redis_url
        )
        
        rag_systems[wsl_path] = rag_system
        current_project = wsl_path  # Set as current project

        # Start file watcher if enabled
        logger.info(f"File watcher enabled: {settings.file_watcher_enabled}")
        if settings.file_watcher_enabled:
            logger.info(f"Starting file watcher for: {wsl_path}")
            file_watcher_manager.start_watching(
                project_path=wsl_path,
                rag_system=rag_system,
                debounce_seconds=settings.file_watcher_debounce_seconds,
                file_extensions=set(request.file_extensions) if request.file_extensions else None
            )
            logger.info(f"File watcher started for: {wsl_path}")

        background_tasks.add_task(
            rag_system.index_project,
            file_extensions=request.file_extensions,
            force_reindex=request.force_reindex
        )

        return {
            "status": "indexing_started",
            "message": f"Project indexing started: {wsl_path}",
            "project_path": wsl_path,
            "file_extensions": request.file_extensions,
            "total_projects": len(rag_systems)
        }
        
    except Exception as e:
        logger.error(f"Indexing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_with_context(request: QueryRequest):
    global rag_systems, current_project
    
    if not rag_systems:
        raise HTTPException(status_code=400, detail="No project indexed. Use POST /index first")
    
    # Determine which project to query
    target_project = request.project_path
    if target_project:
        # Convert to WSL path if needed
        target_project = convert_windows_path_to_wsl(target_project)
        if target_project not in rag_systems:
            raise HTTPException(
                status_code=404, 
                detail=f"Project not indexed: {target_project}. Available: {list(rag_systems.keys())}"
            )
    else:
        # Use current project
        if not current_project or current_project not in rag_systems:
            # Fallback to first available project
            current_project = list(rag_systems.keys())[0]
        target_project = current_project
    
    rag_system = rag_systems[target_project]
    
    try:
        logger.info(f"Processing query for project '{target_project}': {request.query[:100]}...")
        
        optimized_prompt = rag_system.query(
            query=request.query,
            max_results=request.max_results
        )
        
        search_results = rag_system.vector_store.search_similar(request.query, request.max_results)
        context_chunks = len(search_results.get("documents", [[]])[0]) if search_results.get("documents") else 0
        token_count = rag_system.context_manager.count_tokens(optimized_prompt)
        
        metadata = None
        if request.include_metadata:
            metadata = {
                "project_root": str(rag_system.project_root),
                "queried_project": target_project,
                "indexed_files": rag_system.get_indexed_file_count(),
                "total_chunks": rag_system.get_total_chunk_count(),
                "embedding_model": settings.embedding_model,
                "available_projects": list(rag_systems.keys())
            }
        
        return QueryResponse(
            optimized_prompt=optimized_prompt,
            context_chunks=context_chunks,
            token_count=token_count,
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"Query error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/stats")
async def get_statistics(project_path: Optional[str] = None):
    """Get statistics for a specific project or current project"""
    global rag_systems, current_project
    
    if not rag_systems:
        raise HTTPException(status_code=400, detail="No project indexed")
    
    # Determine which project
    target_project = project_path
    if target_project:
        target_project = convert_windows_path_to_wsl(target_project)
        if target_project not in rag_systems:
            raise HTTPException(status_code=404, detail=f"Project not found: {target_project}")
    else:
        target_project = current_project or list(rag_systems.keys())[0]
    
    rag_system = rag_systems[target_project]
    
    return {
        "project_root": str(rag_system.project_root),
        "indexed_files": rag_system.get_indexed_file_count(),
        "total_chunks": rag_system.get_total_chunk_count(),
        "vector_db_size": rag_system.get_vector_db_size(),
        "embedding_model": settings.embedding_model,
        "is_current": target_project == current_project,
        "all_projects": list(rag_systems.keys())
    }

@app.get("/projects")
async def list_projects():
    """List all indexed projects"""
    global rag_systems, current_project
    
    projects = []
    for path, rag_sys in rag_systems.items():
        projects.append({
            "path": path,
            "name": Path(path).name,
            "indexed_files": rag_sys.get_indexed_file_count(),
            "total_chunks": rag_sys.get_total_chunk_count(),
            "is_current": path == current_project
        })
    
    return {
        "total_projects": len(projects),
        "current_project": current_project,
        "projects": projects
    }

@app.post("/switch")
async def switch_project(request: SwitchRequest):
    """Switch the current/active project"""
    global rag_systems, current_project
    
    wsl_path = convert_windows_path_to_wsl(request.project_path)
    
    if wsl_path not in rag_systems:
        raise HTTPException(
            status_code=404,
            detail=f"Project not indexed: {wsl_path}. Index it first with POST /index"
        )
    
    current_project = wsl_path
    logger.info(f"Switched current project to: {current_project}")
    return {
        "status": "switched",
        "current_project": current_project,
        "message": f"Switched to project: {wsl_path}"
    }

@app.delete("/clear")
async def clear_index(project_path: Optional[str] = None):
    """Clear a specific project or all projects"""
    global rag_systems, current_project
    
    if not rag_systems:
        return {"status": "no_index", "message": "No index to clear"}
    
    if project_path:
        # Clear specific project
        wsl_path = convert_windows_path_to_wsl(project_path)
        if wsl_path in rag_systems:
            rag_systems[wsl_path].clear_cache()
            del rag_systems[wsl_path]
            file_watcher_manager.stop_watching(wsl_path)
            if current_project == wsl_path:
                current_project = list(rag_systems.keys())[0] if rag_systems else None
            return {"status": "cleared", "message": f"Project cleared: {wsl_path}"}
        else:
            raise HTTPException(status_code=404, detail=f"Project not found: {wsl_path}")
    else:
        # Clear all projects
        for rag_sys in rag_systems.values():
            rag_sys.clear_cache()
        rag_systems.clear()
        file_watcher_manager.stop_all()
        current_project = None
        return {"status": "cleared", "message": "All projects cleared"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
