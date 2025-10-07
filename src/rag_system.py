"""# TEST: File watcher automatikus reindexelés teszt - MÓDOSÍTVA 3 - TESZT MOST!"""

"""Core RAG System Implementation"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
import hashlib
import json

from .vector_store import VectorStore
from .context_manager import ContextManager
from .code_parser import CodeParser
from .cache_manager import CacheManager

logger = logging.getLogger(__name__)


class LocalRAGSystem:
    """Main RAG system orchestrator"""
    
    def __init__(
        self,
        project_root: str,
        vector_db_path: str = "/app/data/chroma_db",
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
        redis_url: Optional[str] = None,
        max_context_tokens: int = 4000
    ):
        self.project_root = Path(project_root)
        self.vector_db_path = Path(vector_db_path)
        self.embedding_model = embedding_model
        self.max_context_tokens = max_context_tokens
        
        # Generate project-specific collection name
        project_name = self.project_root.name
        project_hash = hashlib.sha256(str(self.project_root).encode()).hexdigest()[:8]
        collection_name = f"code_chunks_{project_name}_{project_hash}"
        
        # Initialize components
        self.vector_store = VectorStore(
            db_path=str(self.vector_db_path),
            embedding_model=embedding_model,
            collection_name=collection_name
        )
        
        self.context_manager = ContextManager(
            max_tokens=max_context_tokens
        )
        
        self.code_parser = CodeParser()
        
        self.cache_manager = CacheManager(redis_url=redis_url) if redis_url else None
        self._project_id = str(self.project_root)
        
        # Persistent metadata file path
        self._metadata_file = self.vector_db_path / f"metadata_{collection_name}.json"
        
        # Load or initialize indexed files tracking
        self._indexed_files = self._load_metadata()  # file_path: file_hash
        self._total_chunks = 0
        
        logger.info(f"RAG System initialized for project: {self.project_root}")
        if self._indexed_files:
            logger.info(f"Loaded {len(self._indexed_files)} previously indexed files from metadata")
    
    def index_project(
        self,
        file_extensions: List[str] = None,
        force_reindex: bool = False
    ) -> Dict[str, Any]:
        """Index all relevant files in the project"""
        if file_extensions is None:
            file_extensions = [
                ".py", ".js", ".ts", ".jsx", ".tsx", 
                ".java", ".cs", ".cpp", ".h", ".go", ".rs",
                ".vue", ".rb", ".php", ".swift", ".kt"
            ]
        
        logger.info(f"Starting indexing with extensions: {file_extensions}")
        
        files_to_index = []
        for ext in file_extensions:
            files_to_index.extend(self.project_root.rglob(f"*{ext}"))
        
        # Filter out common directories to skip
        skip_dirs = {
            "node_modules", ".git", "__pycache__", "venv", "env",
            "dist", "build", ".next", "target", "bin", "obj"
        }
        
        files_to_index = [
            f for f in files_to_index 
            if not any(skip in f.parts for skip in skip_dirs)
        ]
        
        logger.info(f"Found {len(files_to_index)} files to process")
        
        indexed_count = 0
        chunk_count = 0
        
        for file_path in files_to_index:
            try:
                # Check if file needs reindexing
                file_hash = self._get_file_hash(file_path)
                
                if not force_reindex and str(file_path) in self._indexed_files:
                    if self._indexed_files[str(file_path)] == file_hash:
                        logger.debug(f"Skipping unchanged file: {file_path}")
                        continue
                
                # Read and parse file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Parse code into chunks
                chunks = self.code_parser.parse_file(content, file_path.suffix)
                
                # Add metadata to chunks
                for i, chunk in enumerate(chunks):
                    chunk['file_path'] = str(file_path.relative_to(self.project_root))
                    chunk['full_path'] = str(file_path)
                    chunk['chunk_index'] = i
                    chunk['file_extension'] = file_path.suffix
                
                # Store in vector database
                self.vector_store.add_documents(chunks)
                
                self._indexed_files[str(file_path)] = file_hash
                indexed_count += 1
                chunk_count += len(chunks)
                
                if indexed_count % 10 == 0:
                    logger.info(f"Indexed {indexed_count}/{len(files_to_index)} files...")
                
            except Exception as e:
                logger.error(f"Error indexing {file_path}: {str(e)}")
                continue
        
        self._total_chunks = chunk_count
        
        # Save metadata after indexing
        self._save_metadata()
        
        logger.info(f"Indexing complete: {indexed_count} files, {chunk_count} chunks")
        
        return {
            "indexed_files": indexed_count,
            "total_chunks": chunk_count,
            "skipped_files": len(files_to_index) - indexed_count
        }
    
    def query(
        self,
        query: str,
        max_results: int = 5
    ) -> str:
        """Query the RAG system and return optimized context"""
        
        # Check cache first
        if self.cache_manager:
            cached_result = self.cache_manager.get(self._project_id, query)
            if cached_result:
                logger.info("Returning cached result")
                return cached_result
        
        # Search vector store
        search_results = self.vector_store.search_similar(query, max_results)
        
        if not search_results or not search_results.get("documents"):
            logger.warning("No relevant context found")
            return f"Query: {query}\n\nNo relevant code context found."
        
        # Extract documents and metadata
        documents = search_results["documents"][0]
        metadatas = search_results.get("metadatas", [[]])[0]
        
        # Build optimized context
        optimized_prompt = self.context_manager.build_optimized_context(
            query=query,
            documents=documents,
            metadatas=metadatas
        )
        
        # Cache the result
        if self.cache_manager:
            self.cache_manager.set(self._project_id, query, optimized_prompt, ttl=3600)  # 1 hour
        
        return optimized_prompt
    
    def get_indexed_file_count(self) -> int:
        """Return number of indexed files"""
        return len(self._indexed_files)
    
    def get_total_chunk_count(self) -> int:
        """Return total number of chunks"""
        return self._total_chunks
    
    def get_vector_db_size(self) -> str:
        """Return size of vector database"""
        try:
            total_size = sum(
                f.stat().st_size 
                for f in self.vector_db_path.rglob('*') 
                if f.is_file()
            )
            # Convert to MB
            size_mb = total_size / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        except Exception as e:
            logger.error(f"Error calculating DB size: {e}")
            return "Unknown"
    
    def clear_cache(self):
        """Clear cache for this project only"""
        if self.cache_manager:
            self.cache_manager.clear_all(self._project_id)
        logger.info("Cache cleared for project: %s", self._project_id)
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate hash of file content"""
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                hasher.update(f.read())
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Error hashing file {file_path}: {e}")
            return ""
    
    def _save_metadata(self):
        """Save indexed files metadata to disk"""
        try:
            metadata = {
                "indexed_files": self._indexed_files,
                "total_chunks": self._total_chunks,
                "project_root": str(self.project_root)
            }
            self._metadata_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self._metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"Saved metadata for {len(self._indexed_files)} files")
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def _load_metadata(self) -> dict:
        """Load indexed files metadata from disk"""
        try:
            if self._metadata_file.exists():
                with open(self._metadata_file, 'r') as f:
                    metadata = json.load(f)
                    self._total_chunks = metadata.get("total_chunks", 0)
                    return metadata.get("indexed_files", {})
            return {}
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
            return {}
