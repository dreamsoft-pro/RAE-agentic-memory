import json
from datetime import datetime, timezone
from typing import Any, Optional, List, Dict
from uuid import UUID, uuid4
import asyncpg
from ..interfaces.storage import IMemoryStorage

class PostgreSQLStorage(IMemoryStorage):
    def __init__(self, dsn: str | None = None, pool: Optional[asyncpg.Pool] = None, **pool_kwargs: Any) -> None:
        self.dsn = dsn
        self._pool = pool
        self._pool_kwargs = pool_kwargs
    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None: self._pool = await asyncpg.create_pool(self.dsn, **self._pool_kwargs)
        return self._pool
    async def store_memory(self, **kwargs) -> UUID:
        pool = await self._get_pool(); m_id = uuid4()
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO memories (id, content, layer, tenant_id, agent_id, tags, metadata, importance, created_at, project) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", m_id, kwargs.get("content"), kwargs.get("layer"), kwargs.get("tenant_id"), kwargs.get("agent_id"), kwargs.get("tags", []), json.dumps(kwargs.get("metadata", {})), kwargs.get("importance", 0.5), datetime.now(timezone.utc).replace(tzinfo=None), kwargs.get("project"))
        return m_id
    async def get_memory(self, memory_id: UUID, tenant_id: str) -> dict[str, Any] | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn: row = await conn.fetchrow("SELECT * FROM memories WHERE id = $1 AND tenant_id = $2", memory_id, tenant_id)
        return dict(row) if row else None
    async def list_memories(self, tenant_id: str, **kwargs) -> List[Dict[str, Any]]:
        pool = await self._get_pool()
        async with pool.acquire() as conn: rows = await conn.fetch("SELECT * FROM memories WHERE tenant_id = $1 LIMIT $2", tenant_id, kwargs.get('limit', 100))
        return [dict(r) for r in rows]
    async def search_memories(self, query: str, tenant_id: str, agent_id: str, layer: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        pool = await self._get_pool(); final_query = query
        if '"' not in query: final_query = query.replace(" ", " OR ")
        sql = """SELECT *, ts_rank_cd(to_tsvector('english', coalesce(content, '')), websearch_to_tsquery('english', $1)) as score FROM memories WHERE tenant_id = $2 AND agent_id = $3 AND layer = $4 AND (to_tsvector('english', coalesce(content, '')) @@ websearch_to_tsquery('english', $1) OR content ILIKE $5) ORDER BY score DESC LIMIT $6"""
        async with pool.acquire() as conn: rows = await conn.fetch(sql, final_query, tenant_id, agent_id, layer, f"%{query}%", limit)
        return [dict(r) for r in rows]
    async def delete_memories_with_metadata_filter(self, **kwargs): return 0
    async def count_memories(self, **kwargs): return 0
    async def update_memory_access(self, **kwargs): return True
    async def delete_expired_memories(self, **kwargs): return 0
    async def update_memory(self, **kwargs): return True
    async def delete_memory(self, **kwargs): return True
