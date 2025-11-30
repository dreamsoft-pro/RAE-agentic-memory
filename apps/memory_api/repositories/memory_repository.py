"""
MemoryRepository - Data Access Layer for Memory Operations.

This repository encapsulates all database operations related to memories,
following the Repository/DAO pattern to separate data access from business logic.
"""

from typing import Any, Dict, List, Optional

import asyncpg
import structlog

logger = structlog.get_logger(__name__)


class MemoryRepository:
    """
    Repository for memory data access operations.

    Handles all SQL queries related to memory CRUD operations.
    """

    def __init__(self, pool: asyncpg.Pool):
        """
        Initialize memory repository.

        Args:
            pool: AsyncPG connection pool for database operations
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
        """
        Insert a new memory record into the database.

        Args:
            tenant_id: Tenant identifier for data isolation
            content: Memory content
            source: Source of the memory
            importance: Importance score
            layer: Memory layer (em, sm, rm)
            tags: Optional list of tags
            timestamp: Timestamp of the memory
            project: Project identifier
            metadata: Optional metadata

        Returns:
            Dict containing id, created_at, last_accessed_at, and usage_count
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SET app.tenant_id = $1", tenant_id)

                columns = [
                    "tenant_id",
                    "content",
                    "source",
                    "importance",
                    "layer",
                    "tags",
                    "timestamp",
                    "project",
                ]
                values = [
                    tenant_id,
                    content,
                    source,
                    importance,
                    layer,
                    tags,
                    timestamp,
                    project,
                ]

                if metadata is not None:
                    columns.append("metadata")
                    values.append(asyncpg.types.Jsonb(metadata))

                columns_str = ", ".join(columns)
                placeholders_str = ", ".join([f"${i+1}" for i in range(len(values))])

                sql = f"INSERT INTO memories ({columns_str}) VALUES ({placeholders_str}) RETURNING id, created_at, last_accessed_at, usage_count"

                row = await conn.fetchrow(sql, *values)

                if not row:
                    logger.error(
                        "memory_insert_failed", tenant_id=tenant_id, project=project
                    )
                    return None

                logger.info(
                    "memory_inserted",
                    tenant_id=tenant_id,
                    project=project,
                    memory_id=str(row["id"]),
                )

                return {
                    "id": str(row["id"]),
                    "created_at": row["created_at"],
                    "last_accessed_at": row["last_accessed_at"],
                    "usage_count": row["usage_count"],
                }

    async def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        """
        Delete a memory record from the database.

        Args:
            memory_id: Memory identifier
            tenant_id: Tenant identifier for data isolation

        Returns:
            True if memory was deleted, False if not found
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SET app.tenant_id = $1", tenant_id)
                result = await conn.execute(
                    "DELETE FROM memories WHERE id = $1", memory_id
                )

                deleted = result != "DELETE 0"

                if deleted:
                    logger.info(
                        "memory_deleted", tenant_id=tenant_id, memory_id=memory_id
                    )
                else:
                    logger.warning(
                        "memory_not_found", tenant_id=tenant_id, memory_id=memory_id
                    )

                return deleted

    async def get_memory_by_id(
        self, memory_id: str, tenant_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single memory by its ID.

        Args:
            memory_id: Memory identifier
            tenant_id: Tenant identifier for data isolation

        Returns:
            Memory record dict or None if not found
        """
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                SELECT id, content, source, importance, layer, tags,
                       timestamp, created_at, last_accessed_at, usage_count, project
                FROM memories
                WHERE id = $1 AND tenant_id = $2
                """,
                memory_id,
                tenant_id,
            )

            if not record:
                return None

            return dict(record)

    async def get_semantic_memories(
        self, tenant_id: str, project: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all semantic memories for a tenant and project.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier

        Returns:
            List of semantic memory records
        """
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, content, tags, metadata, layer, created_at
                FROM memories
                WHERE tenant_id = $1 AND project = $2 AND layer = 'sm'
                ORDER BY created_at DESC
                """,
                tenant_id,
                project,
            )
            return [dict(r) for r in records]

    async def get_reflective_memories(
        self, tenant_id: str, project: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all reflective memories for a tenant and project.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier

        Returns:
            List of reflective memory records
        """
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, content, tags, metadata, layer, created_at
                FROM memories
                WHERE tenant_id = $1 AND project = $2 AND layer = 'rm'
                ORDER BY created_at DESC
                """,
                tenant_id,
                project,
            )
            return [dict(r) for r in records]

    async def get_episodic_memories(
        self,
        tenant_id: str,
        project: str,
        limit: Optional[int] = None,
        session_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve episodic memories for a tenant and project.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier
            limit: Optional limit on number of records
            session_id: Optional session identifier filter

        Returns:
            List of episodic memory records
        """
        async with self.pool.acquire() as conn:

            conditions = ["tenant_id = $1", "project = $2", "layer = 'em'"]
            params = [tenant_id, project]

            if session_id:
                conditions.append("metadata->>'session_id' = $" + str(len(params) + 1))
                params.append(str(session_id))

            where_clause = " AND ".join(conditions)

            sql = f"""
                SELECT id, content, tags, metadata, layer, created_at, timestamp, source
                FROM memories
                WHERE {where_clause}
                ORDER BY created_at DESC
            """

            if limit:
                sql += f" LIMIT ${len(params) + 1}"
                params.append(limit)

            records = await conn.fetch(sql, *params)
            return [dict(r) for r in records]

    async def count_memories_by_layer(
        self, tenant_id: str, layer: str, project: Optional[str] = None
    ) -> int:
        """
        Count memories by layer, optionally filtered by project.

        Args:
            tenant_id: Tenant identifier
            layer: Memory layer (em, sm, rm)
            project: Optional project identifier

        Returns:
            Count of memories matching criteria
        """
        async with self.pool.acquire() as conn:
            if project:
                count = await conn.fetchval(
                    """
                    SELECT COUNT(*) FROM memories
                    WHERE layer = $1 AND project = $2 AND tenant_id = $3
                    """,
                    layer,
                    project,
                    tenant_id,
                )
            else:
                count = await conn.fetchval(
                    """
                    SELECT COUNT(*) FROM memories
                    WHERE layer = $1 AND tenant_id = $2
                    """,
                    layer,
                    tenant_id,
                )
            return count

    async def get_average_strength(
        self, tenant_id: str, layer: str, project: Optional[str] = None
    ) -> float:
        """
        Get average strength for memories by layer.

        Args:
            tenant_id: Tenant identifier
            layer: Memory layer
            project: Optional project identifier

        Returns:
            Average strength value (or 0.0 if no memories)
        """
        async with self.pool.acquire() as conn:
            if project:
                avg_strength = await conn.fetchval(
                    """
                    SELECT AVG(strength) FROM memories
                    WHERE layer = $1 AND project = $2 AND tenant_id = $3
                    """,
                    layer,
                    project,
                    tenant_id,
                )
            else:
                avg_strength = await conn.fetchval(
                    """
                    SELECT AVG(strength) FROM memories
                    WHERE layer = $1 AND tenant_id = $2
                    """,
                    layer,
                    tenant_id,
                )
            return float(avg_strength) if avg_strength is not None else 0.0

    async def update_memory_access_stats(
        self, memory_ids: List[str], tenant_id: str
    ) -> int:
        """
        Update access statistics for multiple memories in a single batch operation.

        This method implements efficient batch updates for memory access tracking,
        which is critical for the importance scoring and decay mechanisms.

        Updates performed:
        - Increments usage_count by 1 for each memory
        - Sets last_accessed_at to current UTC timestamp

        Args:
            memory_ids: List of memory IDs to update
            tenant_id: Tenant identifier for security validation

        Returns:
            Number of memories successfully updated

        Notes:
            - Uses batch UPDATE for performance (avoids N queries)
            - Only updates memories belonging to the specified tenant (security)
            - Timestamps are in UTC for consistency
            - Used by agent execution and query flows to track memory usage
        """
        if not memory_ids:
            logger.debug(
                "update_memory_access_stats_skipped", reason="empty_memory_ids"
            )
            return 0

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Security: Set tenant context
                await conn.execute("SET app.tenant_id = $1", tenant_id)

                # Batch update using ANY array
                result = await conn.execute(
                    """
                    UPDATE memories
                    SET
                        usage_count = usage_count + 1,
                        last_accessed_at = $1
                    WHERE
                        id = ANY($2::uuid[])
                        AND tenant_id = $3
                    """,
                    now,
                    memory_ids,
                    tenant_id,
                )

                # Parse result string "UPDATE N" to get count
                updated_count = int(result.split()[-1]) if result else 0

                logger.info(
                    "memory_access_stats_updated",
                    tenant_id=tenant_id,
                    memory_ids_count=len(memory_ids),
                    updated_count=updated_count,
                    timestamp=now.isoformat(),
                )

                return updated_count
