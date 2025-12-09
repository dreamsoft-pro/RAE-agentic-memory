"""
RAE-Core integration service.

Wraps RAEEngine and adapters for use in FastAPI application.
"""

from typing import Optional

import asyncpg
import redis.asyncio as redis
import structlog
from qdrant_client import AsyncQdrantClient

from rae_core.adapters import (
    PostgresMemoryAdapter,
    QdrantVectorAdapter,
    RedisCacheAdapter,
)
from rae_core.engine import RAEEngine
from rae_core.models.memory import QueryMemoryResponse

logger = structlog.get_logger(__name__)


class RAECoreService:
    """
    Integration service for RAE-Core.

    Manages RAEEngine lifecycle and provides high-level API.
    """

    def __init__(
        self,
        postgres_pool: asyncpg.Pool,
        qdrant_client: AsyncQdrantClient,
        redis_client: redis.Redis,
    ):
        """
        Initialize service with infrastructure clients.

        Args:
            postgres_pool: PostgreSQL connection pool
            qdrant_client: Qdrant async client
            redis_client: Redis async client
        """
        self.postgres_pool = postgres_pool
        self.qdrant_client = qdrant_client
        self.redis_client = redis_client

        # Initialize adapters
        self.postgres_adapter = PostgresMemoryAdapter(postgres_pool)
        self.qdrant_adapter = QdrantVectorAdapter(qdrant_client)
        self.redis_adapter = RedisCacheAdapter(redis_client)

        # Initialize RAEEngine
        self.engine = RAEEngine(
            sensory_max_size=100,
            sensory_retention_seconds=30,
            working_max_size=100,
            working_retention_minutes=60,
            enable_auto_consolidation=True,
            enable_reflections=True,
        )

        logger.info("rae_core_service_initialized")

    async def store_memory(
        self,
        tenant_id: str,
        project: str,
        content: str,
        source: str,
        importance: Optional[float] = None,
        tags: Optional[list] = None,
        layer: Optional[str] = None,
    ) -> str:
        """
        Store memory using RAEEngine.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier
            content: Memory content
            source: Memory source
            importance: Importance score (0-1)
            tags: Optional tags
            layer: Target layer (auto if None)

        Returns:
            Memory ID
        """
        # Store in RAEEngine (in-memory layers)
        memory_id = await self.engine.store_memory(
            content=content,
            source=source,
            importance=importance or 0.5,
            layer=layer,
            tags=tags,
            tenant_id=tenant_id,
            project=project,
        )

        # Also persist to PostgreSQL for durability
        await self.postgres_adapter.insert_memory(
            tenant_id=tenant_id,
            content=content,
            source=source,
            importance=importance or 0.5,
            layer=layer or "ltm",
            tags=tags,
            timestamp=None,
            project=project,
        )

        logger.info(
            "memory_stored",
            memory_id=memory_id,
            tenant_id=tenant_id,
            project=project,
            layer=layer,
        )

        return memory_id

    async def query_memories(
        self,
        tenant_id: str,
        project: str,
        query: str,
        k: int = 10,
        layers: Optional[list] = None,
    ) -> QueryMemoryResponse:
        """
        Query memories across layers.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier
            query: Query text
            k: Number of results
            layers: Layers to search (default: all)

        Returns:
            Query response with results
        """
        response = await self.engine.query_memory(
            query=query,
            k=k,
            filters={"project": project},
            search_layers=layers,
        )

        logger.info(
            "memories_queried",
            tenant_id=tenant_id,
            project=project,
            result_count=len(response.results),
        )

        return response

    async def consolidate_memories(
        self,
        tenant_id: str,
        project: str,
    ) -> dict:
        """
        Trigger memory consolidation.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier

        Returns:
            Consolidation statistics
        """
        results = await self.engine.consolidate_memories(
            tenant_id=tenant_id,
            project=project,
        )

        logger.info(
            "memories_consolidated",
            tenant_id=tenant_id,
            project=project,
            results=results,
        )

        return results

    async def generate_reflections(
        self,
        tenant_id: str,
        project: str,
    ) -> list:
        """
        Generate reflections from patterns.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier

        Returns:
            List of generated reflections
        """
        reflections = await self.engine.generate_reflections(
            tenant_id=tenant_id,
            project=project,
        )

        logger.info(
            "reflections_generated",
            tenant_id=tenant_id,
            project=project,
            count=len(reflections),
        )

        return reflections

    async def get_statistics(
        self,
        tenant_id: str,
        project: str,
    ) -> dict:
        """
        Get memory statistics across all layers.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier

        Returns:
            Statistics dictionary
        """
        stats = await self.engine.get_statistics()

        logger.info(
            "statistics_retrieved",
            tenant_id=tenant_id,
            project=project,
            total_memories=stats.get("total_memories", 0),
        )

        return stats

    async def clear_memories(
        self,
        tenant_id: str,
    ) -> dict:
        """
        Clear all memories for tenant.

        Args:
            tenant_id: Tenant identifier

        Returns:
            Clear statistics
        """
        results = await self.engine.clear_all(tenant_id=tenant_id)

        logger.info(
            "memories_cleared",
            tenant_id=tenant_id,
            results=results,
        )

        return results
