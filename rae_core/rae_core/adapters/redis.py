"""
Redis adapter for caching.

Implements caching layer for frequently accessed memories.
"""

import json
from typing import Any, Dict, List, Optional

import redis.asyncio as redis


class RedisCacheAdapter:
    """
    Redis adapter for memory caching.

    Provides fast access to frequently used memories.
    """

    def __init__(
        self,
        redis_client: redis.Redis,
        ttl: int = 3600,
        key_prefix: str = "rae:memory:",
    ):
        """
        Initialize adapter with Redis client.

        Args:
            redis_client: Redis async client
            ttl: Time to live in seconds (default: 1 hour)
            key_prefix: Key prefix for namespacing
        """
        self.redis = redis_client
        self.ttl = ttl
        self.key_prefix = key_prefix

    def _make_key(self, memory_id: str, tenant_id: str) -> str:
        """Generate cache key."""
        return f"{self.key_prefix}{tenant_id}:{memory_id}"

    async def get_memory(
        self, memory_id: str, tenant_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get memory from cache."""
        key = self._make_key(memory_id, tenant_id)
        data = await self.redis.get(key)

        if not data:
            return None

        return json.loads(data)

    async def set_memory(
        self,
        memory_id: str,
        tenant_id: str,
        memory_data: Dict[str, Any],
        ttl: Optional[int] = None,
    ) -> bool:
        """Set memory in cache."""
        key = self._make_key(memory_id, tenant_id)
        serialized = json.dumps(memory_data, default=str)

        await self.redis.set(
            key,
            serialized,
            ex=ttl or self.ttl,
        )

        return True

    async def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        """Delete memory from cache."""
        key = self._make_key(memory_id, tenant_id)
        result = await self.redis.delete(key)
        return result > 0

    async def get_many(
        self, memory_ids: List[str], tenant_id: str
    ) -> Dict[str, Dict[str, Any]]:
        """Get multiple memories from cache."""
        if not memory_ids:
            return {}

        keys = [self._make_key(mid, tenant_id) for mid in memory_ids]
        values = await self.redis.mget(keys)

        results = {}
        for memory_id, value in zip(memory_ids, values):
            if value:
                results[memory_id] = json.loads(value)

        return results

    async def set_many(
        self,
        memories: Dict[str, Dict[str, Any]],
        tenant_id: str,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set multiple memories in cache."""
        if not memories:
            return True

        pipe = self.redis.pipeline()

        for memory_id, memory_data in memories.items():
            key = self._make_key(memory_id, tenant_id)
            serialized = json.dumps(memory_data, default=str)
            pipe.set(key, serialized, ex=ttl or self.ttl)

        await pipe.execute()
        return True

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        full_pattern = f"{self.key_prefix}{pattern}"
        cursor = 0
        deleted = 0

        while True:
            cursor, keys = await self.redis.scan(
                cursor=cursor,
                match=full_pattern,
                count=100,
            )

            if keys:
                deleted += await self.redis.delete(*keys)

            if cursor == 0:
                break

        return deleted

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        info = await self.redis.info("stats")

        return {
            "total_keys": await self.redis.dbsize(),
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "evicted": info.get("evicted_keys", 0),
        }

    async def clear_tenant_cache(self, tenant_id: str) -> int:
        """Clear all cache entries for a tenant."""
        pattern = f"{tenant_id}:*"
        return await self.invalidate_pattern(pattern)
