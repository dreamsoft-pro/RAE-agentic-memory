"""
PostgreSQL adapter for memory storage.

Implements MemoryRepositoryProtocol using asyncpg.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

import asyncpg

from rae_core.interfaces.repository import MemoryRepositoryProtocol


class PostgresMemoryAdapter:
    """
    PostgreSQL adapter for memory operations.

    Uses asyncpg connection pool for efficient database access.
    """

    def __init__(self, pool: asyncpg.Pool):
        """
        Initialize adapter with connection pool.

        Args:
            pool: asyncpg connection pool
        """
        self.pool = pool

    async def insert_memory(
        self,
        tenant_id: str,
        content: str,
        source: str,
        importance: float,
        layer: Optional[str],
        tags: Optional[List[str]],
        timestamp: Any,
        project: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Insert memory into PostgreSQL."""
        memory_id = f"mem_{uuid4().hex[:12]}"

        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                INSERT INTO memories (
                    id, tenant_id, content, source, importance,
                    layer, tags, timestamp, project, metadata,
                    created_at, last_accessed_at, usage_count
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $11, 0)
                RETURNING id, created_at, last_accessed_at, usage_count
                """,
                memory_id,
                tenant_id,
                content,
                source,
                importance,
                layer or "ltm",
                tags or [],
                timestamp if isinstance(timestamp, datetime) else datetime.now(),
                project,
                metadata or {},
                datetime.now(),
            )

        return {
            "id": record["id"],
            "created_at": record["created_at"],
            "last_accessed_at": record["last_accessed_at"],
            "usage_count": record["usage_count"],
        }

    async def get_memory_by_id(
        self, memory_id: str, tenant_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve memory by ID."""
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                SELECT
                    id, tenant_id, content, source, importance,
                    layer, tags, timestamp, project, metadata,
                    created_at, last_accessed_at, usage_count
                FROM memories
                WHERE id = $1 AND tenant_id = $2
                """,
                memory_id,
                tenant_id,
            )

        if not record:
            return None

        return dict(record)

    async def query_memories(
        self,
        tenant_id: str,
        project: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Query memories with filters."""
        conditions = ["tenant_id = $1", "project = $2"]
        params: List[Any] = [tenant_id, project]
        param_idx = 3

        if filters:
            if "layer" in filters:
                conditions.append(f"layer = ${param_idx}")
                params.append(filters["layer"])
                param_idx += 1

            if "tags" in filters:
                conditions.append(f"tags && ${param_idx}")
                params.append(filters["tags"])
                param_idx += 1

            if "min_importance" in filters:
                conditions.append(f"importance >= ${param_idx}")
                params.append(filters["min_importance"])
                param_idx += 1

        where_clause = " AND ".join(conditions)
        params.append(limit)

        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                f"""
                SELECT
                    id, tenant_id, content, source, importance,
                    layer, tags, timestamp, project, metadata,
                    created_at, last_accessed_at, usage_count
                FROM memories
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT ${param_idx}
                """,
                *params,
            )

        return [dict(r) for r in records]

    async def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        """Delete memory."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                """
                DELETE FROM memories
                WHERE id = $1 AND tenant_id = $2
                """,
                memory_id,
                tenant_id,
            )

        return result == "DELETE 1"

    async def update_memory_access(self, memory_id: str, tenant_id: str) -> None:
        """Update access timestamp and count."""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE memories
                SET
                    last_accessed_at = $1,
                    usage_count = usage_count + 1
                WHERE id = $2 AND tenant_id = $3
                """,
                datetime.now(),
                memory_id,
                tenant_id,
            )
