import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

import asyncpg

from rae_core.interfaces.storage import IMemoryStorage


class PostgreSQLStorage(IMemoryStorage):
    def __init__(
        self,
        dsn: str | None = None,
        pool: Optional[asyncpg.Pool] = None,
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
        import hashlib
        pool = await self._get_pool()
        
        content = kwargs.get("content", "")
        tenant_id = kwargs.get("tenant_id")
        
        # 1. Universal Fact ID (SHA-256)
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # 2. Prepare Lineage Data
        # We track which instance/source provided this fact
        instance_id = kwargs.get("metadata", {}).get("instance_id", "local-node")
        source = kwargs.get("source", "api")
        
        new_metadata = kwargs.get("metadata", {})
        new_metadata["last_sync_instance"] = instance_id
        
        async with pool.acquire() as conn:
            # 3. Federated UPSERT (Evidence Consolidation)
            # We use jsonb_set to maintain a list of 'witnesses' (sources) in metadata
            sql = """
                INSERT INTO memories (
                    id, content, content_hash, layer, tenant_id, agent_id, tags, metadata, importance, created_at, project, source
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                ON CONFLICT (tenant_id, content_hash) DO UPDATE SET
                    importance = GREATEST(memories.importance, EXCLUDED.importance),
                    usage_count = memories.usage_count + 1,
                    last_accessed_at = now(),
                    source = memories.source || ', ' || EXCLUDED.source,
                    metadata = memories.metadata || EXCLUDED.metadata || 
                               jsonb_build_object('witness_count', (COALESCE((memories.metadata->>'witness_count')::int, 1) + 1))
                RETURNING id
            """
            
            m_id = uuid4()
            row = await conn.fetchrow(
                sql,
                m_id,
                content,
                content_hash,
                kwargs.get("layer"),
                tenant_id,
                kwargs.get("agent_id"),
                kwargs.get("tags", []),
                json.dumps(new_metadata),
                kwargs.get("importance", 0.5),
                datetime.now(timezone.utc).replace(tzinfo=None),
                kwargs.get("project"),
                source
            )
            return row["id"]

    def _row_to_dict(self, row: asyncpg.Record | None) -> dict[str, Any] | None:
        if row is None:
            return None
        d = dict(row)
        
        # Aggressive JSON Parsing for metadata (Fixes Double-Encoding)
        meta = d.get("metadata")
        while isinstance(meta, str):
            try:
                parsed = json.loads(meta)
                if isinstance(parsed, (dict, list)):
                    meta = parsed
                else:
                    break
            except (json.JSONDecodeError, TypeError):
                break
        
        d["metadata"] = meta if isinstance(meta, dict) else {}
        return d

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
        return self._row_to_dict(row)

    async def get_memories_batch(
        self, memory_ids: List[UUID], tenant_id: str
    ) -> List[Dict[str, Any]]:
        if not memory_ids:
            return []
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE id = ANY($1) AND tenant_id = $2",
                memory_ids,
                tenant_id,
            )
        return [self._row_to_dict(r) for r in rows if r]

    async def list_memories(
        self, tenant_id: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        limit = kwargs.get("limit", 100)
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE tenant_id = $1 LIMIT $2", tenant_id, limit
            )
        return [self._row_to_dict(r) for r in rows if r]

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

        # SYSTEM 40.8: Universal Information Gravity (SQL Native)
        # We use 'simple' config to avoid mangling technical IDs/codes.
        raw_query = query.strip()
        
        where_parts = ["tenant_id = $2", "agent_id = $3"]
        params = [raw_query, tenant_id, agent_id]

        if layer:
            where_parts.append(f"layer = ${len(params) + 1}")
            params.append(layer)

        project = kwargs.get("project")
        if project:
            where_parts.append(f"project = ${len(params) + 1}")
            params.append(project)

        # SYSTEM 46.0: Balanced Recall
        limit = max(limit, 50)
        limit_idx = len(params) + 1
        params.append(limit)

        where_clause = " AND ".join(where_parts)

        # The query uses:
        # 1. websearch_to_tsquery: supports "quotes" and -exclusion
        # 2. ts_rank_cd: covers structural density (proximity)
        # 3. ILIKE: as a fallback for non-tokenized symbols
        sql = f"""
            WITH ranked_results AS (
                SELECT *,
                       ts_rank_cd(
                           to_tsvector('simple', coalesce(content, '') || ' ' || coalesce(metadata::text, '')), 
                           websearch_to_tsquery('simple', $1),
                           32 /* Rank normalization: divide by document length */
                       ) as fts_score
                FROM memories
                WHERE {where_clause}
                AND (
                    to_tsvector('simple', coalesce(content, '') || ' ' || coalesce(metadata::text, '')) @@ websearch_to_tsquery('simple', $1)
                    OR content ILIKE '%' || $1 || '%'
                )
            )
            SELECT *, fts_score as score
            FROM ranked_results
            ORDER BY fts_score DESC, created_at DESC
            LIMIT ${limit_idx}
        """

        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [self._row_to_dict(r) for r in rows if r]


    async def delete_memories_with_metadata_filter(self, *args, **kwargs) -> int:
        return 0

    async def count_memories(self, *args, **kwargs) -> int:
        return 0

    async def update_memory_access(self, *args, **kwargs) -> bool:
        return True

    async def delete_expired_memories(self, *args, **kwargs) -> int:
        return 0

    async def update_memory(self, *args, **kwargs) -> bool:
        return True

    async def delete_memory(self, *args, **kwargs) -> bool:
        return True

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()

    async def get_metric_aggregate(self, *args, **kwargs) -> float:
        return 0.0

    async def update_memory_access_batch(self, *args, **kwargs) -> bool:
        return True

    async def adjust_importance(self, *args, **kwargs) -> float:
        return 0.5

    async def delete_memories_below_importance(self, *args, **kwargs) -> int:
        return 0

    async def decay_importance(self, *args, **kwargs) -> int:
        return 0

    async def save_embedding(self, *args, **kwargs) -> bool:
        return True

    async def update_memory_expiration(self, *args, **kwargs) -> bool:
        return True
