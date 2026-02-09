import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

import asyncpg

from rae_core.interfaces.storage import IMemoryStorage


class PostgreSQLStorage(IMemoryStorage):
    def __init__(
        self, dsn: str | None = None, pool: Optional[asyncpg.Pool] = None, **pool_kwargs: Any
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

    async def get_memory(self, memory_id: UUID, tenant_id: str) -> dict[str, Any] | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM memories WHERE id = $1 AND tenant_id = $2",
                memory_id,
                tenant_id,
            )
        return dict(row) if row else None

    async def get_memories_batch(self, memory_ids: List[UUID], tenant_id: str) -> List[Dict[str, Any]]:
        if not memory_ids:
            return []
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM memories WHERE id = ANY($1) AND tenant_id = $2", memory_ids, tenant_id)
        return [dict(r) for r in rows]

    async def list_memories(self, tenant_id: str, **kwargs: Any) -> list[dict[str, Any]]:
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
        layer: Optional[str] = None,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        
        # 1. SETUP BASE PARAMS
        final_query = query.strip()
        where_parts = ["tenant_id = $2", "agent_id = $3"]
        params = [final_query, tenant_id, agent_id] # $1, $2, $3
        
        if layer:
            where_parts.append(f"layer = ${len(params) + 1}")
            params.append(layer)
            
        project = kwargs.get("project")
        if project:
            where_parts.append(f"project = ${len(params) + 1}")
            params.append(project)

        # 2. PREPARE ILIKE KEYWORDS (System 22.1 Restore)
        words = [w.strip() for w in query.split() if len(w.strip()) > 2]
        ilike_clauses = []
        for word in words:
            p_idx = len(params) + 1
            params.append(f"%{word}%")
            ilike_clauses.append(f"(content ILIKE ${p_idx} OR metadata::text ILIKE ${p_idx})")
        
        ilike_all_match = " AND ".join(ilike_clauses) if ilike_clauses else "TRUE"
        
        # 3. FINAL LIMIT
        limit_idx = len(params) + 1
        params.append(limit)

        where_clause = " AND ".join(where_parts)
        
        # 4. EXECUTE HOLISTIC SQL (Facts + Rank + Importance)
        sql = f"""
            SELECT *, 
                   (ts_rank_cd(to_tsvector('simple', coalesce(content, '')), websearch_to_tsquery('simple', $1)) +
                    CASE WHEN {ilike_all_match} THEN 20.0 ELSE 0.0 END +
                    (importance * 2.0)) as score 
            FROM memories 
            WHERE {where_clause} 
            AND (to_tsvector('simple', coalesce(content, '')) @@ websearch_to_tsquery('simple', $1) 
                 OR ({ilike_all_match})) 
            ORDER BY score DESC 
            LIMIT ${limit_idx}
        """
        
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [dict(r) for r in rows]

    async def delete_memories_with_metadata_filter(self, *args, **kwargs) -> int: return 0
    async def count_memories(self, *args, **kwargs) -> int: return 0
    async def update_memory_access(self, *args, **kwargs) -> bool: return True
    async def delete_expired_memories(self, *args, **kwargs) -> int: return 0
    async def update_memory(self, *args, **kwargs) -> bool: return True
    async def delete_memory(self, *args, **kwargs) -> bool: return True
    async def close(self) -> None:
        if self._pool: await self._pool.close()
    async def get_metric_aggregate(self, *args, **kwargs) -> float: return 0.0
    async def update_memory_access_batch(self, *args, **kwargs) -> bool: return True
    async def adjust_importance(self, *args, **kwargs) -> float: return 0.5
    async def delete_memories_below_importance(self, *args, **kwargs) -> int: return 0
    async def decay_importance(self, *args, **kwargs) -> int: return 0
    async def save_embedding(self, *args, **kwargs) -> bool: return True
    async def update_memory_expiration(self, *args, **kwargs) -> bool: return True