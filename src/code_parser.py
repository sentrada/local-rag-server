"""Code Parser for intelligent chunking"""

import logging
from typing import List, Dict, Any
import re

logger = logging.getLogger(__name__)


class CodeParser:
    """Parse source code files into intelligent chunks"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def parse_file(self, content: str, file_extension: str) -> List[Dict[str, Any]]:
        """Parse file content into chunks with metadata"""
        
        # Choose parsing strategy based on file type
        if file_extension in ['.py']:
            return self._parse_python(content)
        elif file_extension in ['.js', '.ts', '.jsx', '.tsx']:
            return self._parse_javascript(content)
        elif file_extension in ['.java', '.cs', '.cpp', '.c', '.h']:
            return self._parse_c_like(content)
        else:
            # Generic chunking for unknown file types
            return self._parse_generic(content)
    
    def _parse_python(self, content: str) -> List[Dict[str, Any]]:
        """Parse Python code into semantic chunks"""
        chunks = []
        lines = content.split('\n')
        
        # Try to identify functions and classes
        current_chunk = []
        current_metadata = {}
        in_function = False
        in_class = False
        indent_level = 0
        start_line = 1
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.lstrip()
            
            # Detect class definition
            if stripped.startswith('class '):
                if current_chunk:
                    chunks.append(self._create_chunk(
                        current_chunk, start_line, line_num - 1, current_metadata
                    ))
                current_chunk = [line]
                match = re.match(r'class\s+(\w+)', stripped)
                current_metadata = {'class_name': match.group(1) if match else 'Unknown'}
                in_class = True
                indent_level = len(line) - len(stripped)
                start_line = line_num
            
            # Detect function definition
            elif stripped.startswith('def '):
                if current_chunk and not in_class:
                    chunks.append(self._create_chunk(
                        current_chunk, start_line, line_num - 1, current_metadata
                    ))
                    current_chunk = []
                    start_line = line_num
                
                match = re.match(r'def\s+(\w+)', stripped)
                if in_class:
                    current_metadata['function_name'] = match.group(1) if match else 'Unknown'
                else:
                    current_metadata = {'function_name': match.group(1) if match else 'Unknown'}
                    in_function = True
                    indent_level = len(line) - len(stripped)
                
                current_chunk.append(line)
            
            # Check if we're exiting a function/class (dedent to same or less level)
            elif (in_function or in_class) and stripped and not stripped.startswith('#'):
                current_indent = len(line) - len(stripped)
                if current_indent <= indent_level and line_num > start_line + 1:
                    # End of function/class
                    chunks.append(self._create_chunk(
                        current_chunk, start_line, line_num - 1, current_metadata
                    ))
                    current_chunk = [line]
                    current_metadata = {}
                    in_function = False
                    in_class = False
                    start_line = line_num
                else:
                    current_chunk.append(line)
            else:
                current_chunk.append(line)
            
            # If chunk is getting too large, split it
            if len('\n'.join(current_chunk)) > self.chunk_size:
                chunks.append(self._create_chunk(
                    current_chunk, start_line, line_num, current_metadata
                ))
                # Keep overlap
                overlap_lines = current_chunk[-5:] if len(current_chunk) > 5 else current_chunk
                current_chunk = overlap_lines
                start_line = line_num - len(overlap_lines) + 1
                current_metadata = {}
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(self._create_chunk(
                current_chunk, start_line, len(lines), current_metadata
            ))
        
        return chunks if chunks else self._parse_generic(content)
    
    def _parse_javascript(self, content: str) -> List[Dict[str, Any]]:
        """Parse JavaScript/TypeScript code"""
        chunks = []
        lines = content.split('\n')
        
        current_chunk = []
        current_metadata = {}
        start_line = 1
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Detect function/class definitions
            if any(keyword in stripped for keyword in ['function ', 'class ', 'const ', 'let ', 'var ']):
                if '=' in stripped or stripped.startswith('function') or stripped.startswith('class'):
                    if current_chunk:
                        chunks.append(self._create_chunk(
                            current_chunk, start_line, line_num - 1, current_metadata
                        ))
                    current_chunk = [line]
                    start_line = line_num
                    
                    # Try to extract name
                    for pattern in [r'function\s+(\w+)', r'class\s+(\w+)', r'(?:const|let|var)\s+(\w+)']:
                        match = re.search(pattern, stripped)
                        if match:
                            current_metadata = {'function_name': match.group(1)}
                            break
            else:
                current_chunk.append(line)
            
            # Split if too large
            if len('\n'.join(current_chunk)) > self.chunk_size:
                chunks.append(self._create_chunk(
                    current_chunk, start_line, line_num, current_metadata
                ))
                overlap_lines = current_chunk[-5:] if len(current_chunk) > 5 else current_chunk
                current_chunk = overlap_lines
                start_line = line_num - len(overlap_lines) + 1
                current_metadata = {}
        
        if current_chunk:
            chunks.append(self._create_chunk(
                current_chunk, start_line, len(lines), current_metadata
            ))
        
        return chunks if chunks else self._parse_generic(content)
    
    def _parse_c_like(self, content: str) -> List[Dict[str, Any]]:
        """Parse C-like languages (Java, C#, C++)"""
        # Similar to JavaScript parsing but with different patterns
        return self._parse_javascript(content)
    
    def _parse_generic(self, content: str) -> List[Dict[str, Any]]:
        """Generic chunking strategy for unknown file types"""
        chunks = []
        lines = content.split('\n')
        
        current_chunk = []
        start_line = 1
        
        for line_num, line in enumerate(lines, 1):
            current_chunk.append(line)
            
            # Split at chunk size with overlap
            if len('\n'.join(current_chunk)) > self.chunk_size:
                chunks.append(self._create_chunk(
                    current_chunk, start_line, line_num, {}
                ))
                
                # Calculate overlap
                overlap_chars = 0
                overlap_lines = []
                for rev_line in reversed(current_chunk):
                    overlap_chars += len(rev_line)
                    overlap_lines.insert(0, rev_line)
                    if overlap_chars >= self.chunk_overlap:
                        break
                
                current_chunk = overlap_lines
                start_line = line_num - len(overlap_lines) + 1
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(self._create_chunk(
                current_chunk, start_line, len(lines), {}
            ))
        
        return chunks
    
    def _create_chunk(
        self,
        lines: List[str],
        start_line: int,
        end_line: int,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a chunk dictionary"""
        content = '\n'.join(lines)
        
        chunk = {
            'content': content,
            'type': 'code',
            'start_line': start_line,
            'end_line': end_line,
            **metadata
        }
        
        return chunk
