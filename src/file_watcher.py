"""File Watcher for automatic project reindexing"""

import logging
import time
import platform
from pathlib import Path
from typing import Optional, Set, Dict
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler, FileSystemEvent

logger = logging.getLogger(__name__)


class ProjectFileWatcher(FileSystemEventHandler):
    """Watches project directories for file changes and triggers reindexing"""
    
    def __init__(
        self,
        rag_system,
        debounce_seconds: float = 2.0,
        file_extensions: Optional[Set[str]] = None
    ):
        """
        Initialize the file watcher
        
        Args:
            rag_system: The RAGSystem instance to reindex files
            debounce_seconds: Time to wait before reindexing after a change
            file_extensions: Set of file extensions to watch (e.g., {'.py', '.cs'})
        """
        super().__init__()
        self.rag_system = rag_system
        self.debounce_seconds = debounce_seconds
        self.file_extensions = file_extensions or {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.cs', '.java', 
            '.cpp', '.h', '.go', '.rs', '.vue', '.php', '.rb'
        }
        
        # Debouncing: track pending changes
        self.pending_changes: Dict[str, float] = {}
        self.last_reindex_time = 0
        
        logger.info(f"File watcher initialized with extensions: {self.file_extensions}")
    
    def _should_process_file(self, file_path: str) -> bool:
        """Check if file should be processed based on extension"""
        path = Path(file_path)
        
        # Ignore hidden files, temp files, and directories
        if path.name.startswith('.') or path.name.endswith('~'):
            return False
        
        # Ignore common non-code directories
        ignore_dirs = {
            '__pycache__', 'node_modules', '.git', '.venv', 'venv',
            'bin', 'obj', 'build', 'dist', '.vs', '.idea'
        }
        if any(ignore_dir in path.parts for ignore_dir in ignore_dirs):
            return False
        
        # Check file extension
        return path.suffix in self.file_extensions
    
    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        if not self._should_process_file(event.src_path):
            return
        
        # Add to pending changes with current timestamp
        self.pending_changes[event.src_path] = time.time()
        logger.info(f"🔔 File modified detected: {event.src_path}")
    
    def on_created(self, event: FileSystemEvent):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        if not self._should_process_file(event.src_path):
            return
        
        self.pending_changes[event.src_path] = time.time()
        logger.info(f"🔔 File created detected: {event.src_path}")
    
    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion events"""
        if event.is_directory:
            return
        
        if not self._should_process_file(event.src_path):
            return
        
        # Remove from vector store
        logger.info(f"File deleted: {event.src_path}")
        try:
            # TODO: Implement vector store deletion by file path
            pass
        except Exception as e:
            logger.error(f"Error removing deleted file from index: {e}")
    
    def process_pending_changes(self):
        """Process pending file changes after debounce period"""
        current_time = time.time()
        files_to_reindex = []
        
        # Find files that have passed the debounce period
        for file_path, change_time in list(self.pending_changes.items()):
            if current_time - change_time >= self.debounce_seconds:
                files_to_reindex.append(file_path)
                del self.pending_changes[file_path]
        
        if not files_to_reindex:
            return
        
        # Avoid reindexing too frequently
        if current_time - self.last_reindex_time < self.debounce_seconds:
            return
        
        # Reindex changed files
        logger.info(f"Reindexing {len(files_to_reindex)} changed file(s)")
        try:
            # For now, trigger a full reindex (can be optimized later)
            self.rag_system.index_project(force_reindex=False)
            self.last_reindex_time = current_time
            logger.info("Reindexing complete")
        except Exception as e:
            logger.error(f"Error during reindexing: {e}", exc_info=True)


class FileWatcherManager:
    """Manages file watchers for multiple projects"""
    
    def __init__(self):
        self.observers: Dict[str, Observer] = {}
        self.watchers: Dict[str, ProjectFileWatcher] = {}
        logger.info("File watcher manager initialized")
    
    def start_watching(
        self,
        project_path: str,
        rag_system,
        debounce_seconds: float = 2.0,
        file_extensions: Optional[Set[str]] = None
    ):
        """Start watching a project directory"""
        
        # Stop existing watcher if any
        if project_path in self.observers:
            self.stop_watching(project_path)
        
        # Create watcher and observer
        watcher = ProjectFileWatcher(
            rag_system=rag_system,
            debounce_seconds=debounce_seconds,
            file_extensions=file_extensions
        )
        
        # Use PollingObserver for Docker/Windows compatibility
        # Regular Observer doesn't receive file system events through Docker volumes on Windows
        logger.info("Using PollingObserver for Docker/Windows compatibility")
        observer = PollingObserver(timeout=1.0)  # Check every 1 second
        observer.schedule(watcher, project_path, recursive=True)
        observer.start()
        
        self.watchers[project_path] = watcher
        self.observers[project_path] = observer
        
        logger.info(f"Started watching: {project_path}")
        return observer
    
    def stop_watching(self, project_path: str):
        """Stop watching a project directory"""
        if project_path in self.observers:
            observer = self.observers[project_path]
            observer.stop()
            observer.join(timeout=5)
            
            del self.observers[project_path]
            del self.watchers[project_path]
            
            logger.info(f"Stopped watching: {project_path}")
    
    def stop_all(self):
        """Stop all watchers"""
        for project_path in list(self.observers.keys()):
            self.stop_watching(project_path)
        logger.info("All watchers stopped")
    
    def process_all_pending_changes(self):
        """Process pending changes for all watchers"""
        for watcher in self.watchers.values():
            watcher.process_pending_changes()
    
    def get_watched_projects(self) -> list:
        """Get list of currently watched projects"""
        return list(self.observers.keys())
