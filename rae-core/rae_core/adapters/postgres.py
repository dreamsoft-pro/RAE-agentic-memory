"""PostgreSQL storage adapter for RAE-core.

Implements IMemoryStorage interface using asyncpg for async PostgreSQL access.
"""

import json
from datetime import datetime, timezone
from typing import Any, Optional, cast
from uuid import UUID, uuid4

try:
    import asyncpg
except ImportError:  # pragma: no cover
    asyncpg = None  # pragma: no cover

from ..interfaces.storage import IMemoryStorage


class PostgreSQLStorage(IMemoryStorage):
    """PostgreSQL implementation of IMemoryStorage."""

    def __init__(
        self,
        dsn: str | None = None,
        pool: Optional["asyncpg.Pool"] = None,
        **pool_kwargs: Any,
    ) -> None:
        if asyncpg is None:
            raise ImportError("asyncpg is required")
        self.dsn = dsn
        self._pool = pool
        self._pool_kwargs = pool_kwargs

    async def _get_pool(self) -> "asyncpg.Pool":
        if self._pool is None:
            if self.dsn is None:
                raise ValueError("Either dsn or pool must be provided")
            self._pool = await asyncpg.create_pool(self.dsn, **self._pool_kwargs)
        return cast("asyncpg.Pool", self._pool)

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def store_memory(self, **kwargs) -> UUID:
        pool = await self._get_pool()
        m_id = uuid4()
        tags = kwargs.get("tags") or []
        meta = kwargs.get("metadata") or {}
        imp = kwargs.get("importance") if kwargs.get("importance") is not None else 0.5
        gov = kwargs.get("governance") or {}
        
        emb_val = str(kwargs.get("embedding")) if kwargs.get("embedding") is not None else None

        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO memories (
                    id, content, layer, tenant_id, agent_id,
                    tags, metadata, embedding, importance, expires_at,
                    created_at, last_accessed_at, memory_type, usage_count,
                    project, session_id, source, strength, info_class, governance
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $11, $12, 0, $13, $14, $15, $16, $17, $18)
                """,
                m_id, kwargs.get("content"), kwargs.get("layer"), kwargs.get("tenant_id"), 
                kwargs.get("agent_id"), tags, json.dumps(meta), emb_val, imp,
                kwargs.get("expires_at"), datetime.now(timezone.utc).replace(tzinfo=None),
                kwargs.get("memory_type", "text"), kwargs.get("project"), kwargs.get("session_id"),
                kwargs.get("source"), kwargs.get("strength", 1.0), kwargs.get("info_class", "internal"),
                json.dumps(gov)
            )
        return m_id

    async def get_memory(self, memory_id: UUID, tenant_id: str) -> dict[str, Any] | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM memories WHERE id = $1 AND tenant_id = $2", memory_id, tenant_id
            )
        if not row: return None
        return {
            "id": row["id"], "content": row["content"], "layer": row["layer"],
            "importance": float(row["importance"] or 0.5), "metadata": row["metadata"] or {},
            "usage_count": row["usage_count"], "created_at": row["created_at"]
        }

    async def list_memories(
        self,
        tenant_id: str,
        agent_id: str | None = None,
        layer: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        project: str | None = None,
        query: str | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        conditions = ["tenant_id = $1"]
        params: list[Any] = [tenant_id]
        idx = 2

        p_filter = project or (filters or {}).get("project")
        if p_filter and p_filter != "default":
            conditions.append(f"project = ${idx}"); params.append(p_filter); idx += 1
        if agent_id:
            conditions.append(f"agent_id = ${idx}"); params.append(agent_id); idx += 1
        if layer:
            conditions.append(f"layer = ${idx}"); params.append(layer); idx += 1

        score_clause = "1.0 as score"
        order_clause = "ORDER BY created_at DESC"

        if query and query.strip():
            if query == "*":
                score_clause = "1.0 as score"
            else:
                # SYSTEM 10.2: Pure Signal Contrast
                # We return raw ts_rank to allow LogicGateway to perform gradient analysis.
                final_query = query
                if '"' not in query:
                    final_query = query.replace(" ", " OR ")
                
                conditions.append(
                    f"(to_tsvector('english', coalesce(content, '')) @@ websearch_to_tsquery('english', ${idx}) OR content ILIKE ${idx+1})"
                )
                
                score_clause = f"""
                    CASE
                        WHEN to_tsvector('english', coalesce(content, '')) @@ websearch_to_tsquery('english', ${idx})
                        THEN ts_rank_cd(to_tsvector('english', coalesce(content, '')), websearch_to_tsquery('english', ${idx}))
                        WHEN content ILIKE ${idx+1} THEN 0.1
                        ELSE 0.01
                    END as score
                """
                params.append(final_query)
                params.append(f"%{query}%")
                idx += 2
                order_clause = "ORDER BY score DESC, importance DESC"

        where_clause = " AND ".join(conditions)
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                f"SELECT *, {score_clause} FROM memories WHERE {where_clause} {order_clause} LIMIT ${idx} OFFSET ${idx+1}",
                *params, limit, offset
            )

        return [dict(row) for row in rows]

    async def update_memory_access(self, memory_id: UUID, tenant_id: str) -> bool:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE memories SET last_accessed_at = NOW(), usage_count = usage_count + 1 WHERE id = $1 AND tenant_id = $2",
                memory_id, tenant_id
            )
        return True