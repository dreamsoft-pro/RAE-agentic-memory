import json
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import asyncpg

from ..interfaces.storage import IMemoryStorage


class PostgreSQLStorage(IMemoryStorage):
    def __init__(
        self,
        dsn: str | None = None,
        pool: asyncpg.Pool | None = None,
        **pool_kwargs: Any,
    ) -> None:
        self.dsn = dsn
        self._pool = pool
        self._pool_kwargs = pool_kwargs

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            if not self.dsn and not self._pool:
                raise ValueError("Either dsn or pool must be provided")
            self._pool = await asyncpg.create_pool(self.dsn, **self._pool_kwargs)
        return self._pool

    async def store_memory(self, **kwargs: Any) -> UUID:
        pool = await self._get_pool()
        m_id = uuid4()
        async with pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO memories (id, content, layer, tenant_id, agent_id, tags, metadata, importance, created_at, project) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)",
                m_id,
                kwargs.get("content"),
                kwargs.get("layer"),
                kwargs.get("tenant_id"),
                kwargs.get("agent_id"),
                kwargs.get("tags", []),
                json.dumps(kwargs.get("metadata", {})),
                kwargs.get("importance", 0.5),
                datetime.now(timezone.utc).replace(tzinfo=None),
                kwargs.get("project"),
            )
        return m_id

    async def get_memory(
        self, memory_id: UUID, tenant_id: str
    ) -> dict[str, Any] | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM memories WHERE id = $1 AND tenant_id = $2",
                memory_id,
                tenant_id,
            )
        return dict(row) if row else None

    async def list_memories(
        self, tenant_id: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        limit = kwargs.get("limit", 100)
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE tenant_id = $1 LIMIT $2", tenant_id, limit
            )
        return [dict(r) for r in rows]

    async def search_memories(
        self,
        query: str,
        tenant_id: str,
        agent_id: str,
        layer: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        final_query = query
        if '"' not in query:
            final_query = query.replace(" ", " OR ")
        sql = """SELECT *, ts_rank_cd(to_tsvector('english', coalesce(content, '')), websearch_to_tsquery('english', $1)) as score FROM memories WHERE tenant_id = $2 AND agent_id = $3 AND layer = $4 AND (to_tsvector('english', coalesce(content, '')) @@ websearch_to_tsquery('english', $1) OR content ILIKE $5) ORDER BY score DESC LIMIT $6"""
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                sql, final_query, tenant_id, agent_id, layer, f"%{query}%", limit
            )
        return [dict(r) for r in rows]

    async def delete_memories_with_metadata_filter(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        layer: str | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> int:
        return 0

    async def count_memories(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        layer: str | None = None,
    ) -> int:
        return 0

    async def update_memory_access(self, memory_id: UUID, tenant_id: str) -> bool:
        return True

    async def delete_expired_memories(
        self, tenant_id: str, agent_id: str | None = None, layer: str | None = None
    ) -> int:
        return 0

    async def update_memory(
        self, memory_id: UUID, tenant_id: str, updates: dict[str, Any]
    ) -> bool:
        return True

    async def delete_memory(self, memory_id: UUID, tenant_id: str) -> bool:
        return True

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()

    async def get_metric_aggregate(
        self,
        tenant_id: str,
        metric: str,
        func: str,
        filters: dict[str, Any] | None = None,
    ) -> float:
        return 0.0

    async def update_memory_access_batch(
        self, memory_ids: list[UUID], tenant_id: str
    ) -> bool:
        return True

    async def adjust_importance(
        self, memory_id: UUID, delta: float, tenant_id: str
    ) -> float:
        return 0.5

    async def delete_memories_below_importance(
        self, tenant_id: str, agent_id: str, layer: str, importance_threshold: float
    ) -> int:
        return 0

    async def decay_importance(self, tenant_id: str, decay_factor: float) -> int:
        return 0

    async def save_embedding(
        self, memory_id: UUID, model_name: str, embedding: list[float], tenant_id: str
    ) -> bool:
        return True

    async def update_memory_expiration(
        self, memory_id: UUID, tenant_id: str, expires_at: datetime | None
    ) -> bool:
        return True
