"""Utility functions"""

import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def convert_windows_path_to_wsl(windows_path: str) -> str:
    """
    Convert Windows path to WSL path
    Example: C:\\Users\\Name\\Project -> /mnt/c/Users/Name/Project
    """
    # If already a WSL path, return as is
    if windows_path.startswith('/'):
        return windows_path
    
    # Handle Windows paths
    path = windows_path.replace('\\', '/')
    
    # Convert drive letter (C: -> /mnt/c)
    match = re.match(r'^([A-Za-z]):', path)
    if match:
        drive = match.group(1).lower()
        path = f"/mnt/{drive}{path[2:]}"
    
    logger.debug(f"Converted path: {windows_path} -> {path}")
    return path


def convert_wsl_path_to_windows(wsl_path: str) -> str:
    """
    Convert WSL path to Windows path
    Example: /mnt/c/Users/Name/Project -> C:\\Users\\Name\\Project
    """
    # If already a Windows path, return as is
    if re.match(r'^[A-Za-z]:', wsl_path):
        return wsl_path
    
    # Handle WSL paths
    match = re.match(r'^/mnt/([a-z])/', wsl_path)
    if match:
        drive = match.group(1).upper()
        path = wsl_path[7:]  # Remove '/mnt/x'
        path = f"{drive}:{path}"
        path = path.replace('/', '\\')
        logger.debug(f"Converted path: {wsl_path} -> {path}")
        return path
    
    # No conversion needed
    return wsl_path


def validate_project_path(path: str) -> bool:
    """Validate that the project path exists and is accessible"""
    try:
        path_obj = Path(path)
        
        if not path_obj.exists():
            logger.warning(f"Path does not exist: {path}")
            return False
        
        if not path_obj.is_dir():
            logger.warning(f"Path is not a directory: {path}")
            return False
        
        # Check if readable
        try:
            list(path_obj.iterdir())
        except PermissionError:
            logger.warning(f"Permission denied for path: {path}")
            return False
        
        logger.debug(f"Path validated: {path}")
        return True
        
    except Exception as e:
        logger.error(f"Error validating path {path}: {e}")
        return False


def get_file_language(file_extension: str) -> str:
    """Get programming language from file extension"""
    lang_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React',
        '.tsx': 'React TypeScript',
        '.java': 'Java',
        '.cs': 'C#',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C/C++ Header',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.vue': 'Vue',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.md': 'Markdown',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.bash': 'Bash',
    }
    return lang_map.get(file_extension.lower(), 'Unknown')


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def sanitize_metadata(metadata: dict) -> dict:
    """
    Sanitize metadata for ChromaDB storage
    ChromaDB doesn't support nested dicts or None values
    """
    sanitized = {}
    
    for key, value in metadata.items():
        if value is None:
            continue
        
        # Convert to string if complex type
        if isinstance(value, (dict, list)):
            sanitized[key] = str(value)
        else:
            sanitized[key] = value
    
    return sanitized
