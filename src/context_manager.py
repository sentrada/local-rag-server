"""Context Manager for optimizing prompts"""

import logging
from typing import List, Dict, Any, Optional
import tiktoken

logger = logging.getLogger(__name__)


class ContextManager:
    """Manages context optimization and token counting"""
    
    def __init__(self, max_tokens: int = 4000, model: str = "gpt-4"):
        self.max_tokens = max_tokens
        self.model = model
        
        # Initialize tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
            logger.warning(f"Model {model} not found, using cl100k_base encoding")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            return len(self.tokenizer.encode(text))
        except Exception as e:
            logger.error(f"Error counting tokens: {e}")
            # Rough estimate: ~4 chars per token
            return len(text) // 4
    
    def build_optimized_context(
        self,
        query: str,
        documents: List[str],
        metadatas: List[Dict[str, Any]]
    ) -> str:
        """Build optimized context that fits within token limit"""
        
        # Reserve tokens for query and formatting
        query_tokens = self.count_tokens(query)
        formatting_overhead = 200  # Reserve for prompt structure
        available_tokens = self.max_tokens - query_tokens - formatting_overhead
        
        # Start building context
        context_parts = []
        context_parts.append("# Relevant Code Context\n")
        context_parts.append(f"Query: {query}\n\n")
        
        used_tokens = self.count_tokens("".join(context_parts))
        
        # Add documents in order of relevance
        included_files = set()
        
        for doc, metadata in zip(documents, metadatas):
            # Create formatted chunk
            file_path = metadata.get('file_path', 'unknown')
            chunk_type = metadata.get('chunk_type', 'code')
            
            # Build chunk header
            chunk_header = f"\n## File: {file_path}\n"
            
            if metadata.get('function_name'):
                chunk_header += f"Function: {metadata['function_name']}\n"
            if metadata.get('class_name'):
                chunk_header += f"Class: {metadata['class_name']}\n"
            if metadata.get('start_line'):
                chunk_header += f"Lines: {metadata['start_line']}-{metadata.get('end_line', '?')}\n"
            
            chunk_header += f"```{self._get_language_from_extension(metadata.get('file_extension', ''))}\n"
            chunk_footer = "\n```\n"
            
            # Assemble full chunk
            full_chunk = chunk_header + doc + chunk_footer
            chunk_tokens = self.count_tokens(full_chunk)
            
            # Check if we have room
            if used_tokens + chunk_tokens > available_tokens:
                logger.info(f"Token limit reached. Included {len(context_parts) - 2} chunks")
                break
            
            context_parts.append(full_chunk)
            included_files.add(file_path)
            used_tokens += chunk_tokens
        
        # Add summary footer
        context_parts.append(f"\n---\n")
        context_parts.append(f"Included {len(included_files)} files with {len(context_parts) - 3} code chunks.\n")
        context_parts.append(f"Total tokens: ~{used_tokens}\n")
        
        optimized_context = "".join(context_parts)
        
        logger.info(
            f"Built context: {len(included_files)} files, "
            f"{len(context_parts) - 3} chunks, ~{used_tokens} tokens"
        )
        
        return optimized_context
    
    def _get_language_from_extension(self, ext: str) -> str:
        """Map file extension to language identifier for syntax highlighting"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.java': 'java',
            '.cs': 'csharp',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'cpp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.vue': 'vue',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
        }
        return ext_map.get(ext.lower(), '')
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit"""
        try:
            tokens = self.tokenizer.encode(text)
            if len(tokens) <= max_tokens:
                return text
            
            truncated_tokens = tokens[:max_tokens]
            return self.tokenizer.decode(truncated_tokens)
        except Exception as e:
            logger.error(f"Error truncating text: {e}")
            # Rough character-based truncation as fallback
            char_limit = max_tokens * 4
            return text[:char_limit]
