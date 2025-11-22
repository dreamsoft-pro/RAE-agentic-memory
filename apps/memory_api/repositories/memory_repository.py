"""
MemoryRepository - Data Access Layer for Memory Operations.

This repository encapsulates all database operations related to memories,
following the Repository/DAO pattern to separate data access from business logic.
"""

from typing import List, Dict, Any, Optional
import asyncpg
import structlog

from apps.memory_api.models import MemoryRecord

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
        project: str
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

        Returns:
            Dict containing id, created_at, last_accessed_at, and usage_count
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SET app.tenant_id = $1", tenant_id)

                columns = [
                    "tenant_id", "content", "source", "importance",
                    "layer", "tags", "timestamp", "project"
                ]
                values = [
                    tenant_id, content, source, importance,
                    layer, tags, timestamp, project
                ]

                columns_str = ", ".join(columns)
                placeholders_str = ", ".join([f"${i+1}" for i in range(len(values))])

                sql = f"INSERT INTO memories ({columns_str}) VALUES ({placeholders_str}) RETURNING id, created_at, last_accessed_at, usage_count"

                row = await conn.fetchrow(sql, *values)

                if not row:
                    logger.error(
                        "memory_insert_failed",
                        tenant_id=tenant_id,
                        project=project
                    )
                    return None

                logger.info(
                    "memory_inserted",
                    tenant_id=tenant_id,
                    project=project,
                    memory_id=str(row["id"])
                )

                return {
                    "id": str(row["id"]),
                    "created_at": row["created_at"],
                    "last_accessed_at": row["last_accessed_at"],
                    "usage_count": row["usage_count"]
                }

    async def delete_memory(
        self,
        memory_id: str,
        tenant_id: str
    ) -> bool:
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
                    "DELETE FROM memories WHERE id = $1",
                    memory_id
                )

                deleted = result != "DELETE 0"

                if deleted:
                    logger.info(
                        "memory_deleted",
                        tenant_id=tenant_id,
                        memory_id=memory_id
                    )
                else:
                    logger.warning(
                        "memory_not_found",
                        tenant_id=tenant_id,
                        memory_id=memory_id
                    )

                return deleted

    async def get_memory_by_id(
        self,
        memory_id: str,
        tenant_id: str
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
                tenant_id
            )

            if not record:
                return None

            return dict(record)

    async def get_semantic_memories(
        self,
        tenant_id: str,
        project: str
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
                project
            )
            return [dict(r) for r in records]

    async def get_reflective_memories(
        self,
        tenant_id: str,
        project: str
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
                project
            )
            return [dict(r) for r in records]

    async def get_episodic_memories(
        self,
        tenant_id: str,
        project: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve episodic memories for a tenant and project.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier
            limit: Optional limit on number of records

        Returns:
            List of episodic memory records
        """
        async with self.pool.acquire() as conn:
            if limit:
                records = await conn.fetch(
                    """
                    SELECT id, content, tags, metadata, layer, created_at, timestamp, source
                    FROM memories
                    WHERE tenant_id = $1 AND project = $2 AND layer = 'em'
                    ORDER BY created_at DESC
                    LIMIT $3
                    """,
                    tenant_id,
                    project,
                    limit
                )
            else:
                records = await conn.fetch(
                    """
                    SELECT id, content, tags, metadata, layer, created_at, timestamp, source
                    FROM memories
                    WHERE tenant_id = $1 AND project = $2 AND layer = 'em'
                    ORDER BY created_at DESC
                    """,
                    tenant_id,
                    project
                )
            return [dict(r) for r in records]

    async def count_memories_by_layer(
        self,
        tenant_id: str,
        layer: str,
        project: Optional[str] = None
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
                    tenant_id
                )
            else:
                count = await conn.fetchval(
                    """
                    SELECT COUNT(*) FROM memories
                    WHERE layer = $1 AND tenant_id = $2
                    """,
                    layer,
                    tenant_id
                )
            return count

    async def get_average_strength(
        self,
        tenant_id: str,
        layer: str,
        project: Optional[str] = None
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
                    tenant_id
                )
            else:
                avg_strength = await conn.fetchval(
                    """
                    SELECT AVG(strength) FROM memories
                    WHERE layer = $1 AND tenant_id = $2
                    """,
                    layer,
                    tenant_id
                )
            return float(avg_strength) if avg_strength is not None else 0.0
