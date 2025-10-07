"""Cache Manager using Redis"""

import logging
import json
from typing import Optional, Any
import hashlib

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching with Redis for faster query responses"""
    
    def __init__(self, redis_url: Optional[str] = None):
        self.redis_client = None
        
        if redis_url:
            try:
                import redis
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
                # Test connection
                self.redis_client.ping()
                logger.info(f"Redis cache connected: {redis_url}")
            except ImportError:
                logger.warning("Redis package not installed. Install with: pip install redis")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Cache disabled.")
                self.redis_client = None
    
    def _generate_key(self, project_id: str, query: str) -> str:
        """Generate cache key from project and query"""
        # Use hash to create consistent, fixed-length keys
        project_hash = hashlib.sha256(project_id.encode()).hexdigest()[:8]
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        return f"rag:query:{project_hash}:{query_hash}"
    
    def get(self, project_id: str, query: str) -> Optional[str]:
        """Get cached result for query in a project"""
        if not self.redis_client:
            return None
        try:
            key = self._generate_key(project_id, query)
            result = self.redis_client.get(key)
            if result:
                logger.debug(f"Cache hit for project: {project_id}, query: {query[:50]}...")
                return result
            logger.debug(f"Cache miss for project: {project_id}, query: {query[:50]}...")
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, project_id: str, query: str, result: str, ttl: int = 3600) -> bool:
        """Set cached result for a project with TTL (time to live in seconds)"""
        if not self.redis_client:
            return False
        try:
            key = self._generate_key(project_id, query)
            self.redis_client.setex(key, ttl, result)
            logger.debug(f"Cached result for project: {project_id}, query: {query[:50]}... (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, project_id: str, query: str) -> bool:
        """Delete cached result for query in a project"""
        if not self.redis_client:
            return False
        try:
            key = self._generate_key(project_id, query)
            self.redis_client.delete(key)
            logger.debug(f"Deleted cache for project: {project_id}, query: {query[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def clear_all(self, project_id: str = None) -> bool:
        """Clear all cached results, or only for a specific project if project_id is given"""
        if not self.redis_client:
            return False
        try:
            if project_id:
                project_hash = hashlib.sha256(project_id.encode()).hexdigest()[:8]
                pattern = f"rag:query:{project_hash}:*"
            else:
                pattern = "rag:query:*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"Cleared {len(keys)} cached queries for pattern {pattern}")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.redis_client:
            return {"enabled": False}
        
        try:
            info = self.redis_client.info("stats")
            keys_count = len(self.redis_client.keys("rag:query:*"))
            
            return {
                "enabled": True,
                "total_connections": info.get("total_connections_received", 0),
                "cached_queries": keys_count,
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"enabled": True, "error": str(e)}
