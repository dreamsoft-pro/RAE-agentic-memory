from typing import Any

import asyncpg
import redis.asyncio as aioredis
import structlog
from qdrant_client import AsyncQdrantClient

logger = structlog.get_logger(__name__)


class InfrastructureFactory:
    """
    Factory for initializing infrastructure components based on RAE_PROFILE.
    Decouples the application from specific driver instantiation.
    """

    @staticmethod
    async def initialize(app: Any, settings: Any) -> None:
        """
        Initialize infrastructure connections and attach them to app.state.

        Args:
            app: The FastAPI application instance.
            settings: The application settings object.
        """
        profile = getattr(settings, "RAE_PROFILE", "standard")
        logger.info("initializing_infrastructure", profile=profile)

        # 1. Postgres Initialization
        # in Lite mode we might skip or use SQLite (future)
        if profile == "standard":
            logger.info("connecting_postgres", host=settings.POSTGRES_HOST)
            app.state.pool = await asyncpg.create_pool(
                host=settings.POSTGRES_HOST,
                database=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
            )
        else:
            logger.info("postgres_connection_skipped", profile=profile)
            # Ensure attribute exists to avoid AttributeErrors, even if None
            app.state.pool = None

        # 2. Redis Initialization
        if profile == "standard":
            logger.info("connecting_redis", url=settings.REDIS_URL)
            app.state.redis_client = await aioredis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
        else:
            logger.info("redis_connection_skipped", profile=profile)
            app.state.redis_client = None

        # 3. Qdrant Initialization
        if profile == "standard":
            logger.info("connecting_qdrant", host=settings.QDRANT_HOST)
            app.state.qdrant_client = AsyncQdrantClient(
                host=settings.QDRANT_HOST, port=settings.QDRANT_PORT
            )
        else:
            logger.info("qdrant_connection_skipped", profile=profile)
            app.state.qdrant_client = None
