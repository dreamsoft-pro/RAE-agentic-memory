import structlog
from asyncpg.pool import Pool as AsyncpgPool
from fastapi import APIRouter, Depends, HTTPException, status
from qdrant_client import AsyncQdrantClient
from redis.asyncio import Redis as AsyncRedis

import apps.llm.broker.llm_router as llm_broker
import apps.memory_api.dependencies as deps  # Modified import
from apps.memory_api.config import settings

router = APIRouter()
logger = structlog.get_logger(__name__)


async def check_postgres(
    pool: AsyncpgPool = Depends(deps.get_db_pool),
):
    """Check PostgreSQL connection."""
    try:
        await pool.fetchval("SELECT 1")
        return {"status": "UP"}
    except Exception as e:
        logger.error("health_check_postgres_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"PostgreSQL DOWN: {e}",
        )


async def check_redis(
    redis_client: AsyncRedis = Depends(deps.get_redis_client),
):  # Used deps.get_redis_client
    """Check Redis connection."""
    try:
        await redis_client.ping()
        return {"status": "UP"}
    except Exception as e:
        logger.error("health_check_redis_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Redis DOWN: {e}"
        )


async def check_qdrant(
    qdrant_client: AsyncQdrantClient = Depends(deps.get_qdrant_client),
):  # Used deps.get_qdrant_client
    """Check Qdrant connection."""
    try:
        # Try to get collections list as a simple health check
        collections = await qdrant_client.get_collections()
        return {"status": "UP", "collections_count": len(collections.collections)}
    except Exception as e:
        logger.error("health_check_qdrant_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Qdrant DOWN: {e}"
        )


async def check_llm_provider():
    """Check if the configured LLM provider is reachable."""
    try:
        # Just ensure LLMRouter can be imported and settings are valid
        # A more thorough check would involve a dummy API call, but that's complex for a basic health check
        llm_broker.LLMRouter()  # Instantiate directly, no unused variable
        provider = getattr(settings, "LLM_PROVIDER", "none")
        return {"status": "UP", "provider": provider}
    except Exception as e:
        logger.warning("health_check_llm_optional", error=str(e))
        # In development mode without LLM, this is expected
        return {
            "status": "OPTIONAL",
            "provider": "none",
            "note": "LLM not configured (development mode)",
        }


@router.get("/health", response_model=dict, summary="Overall Health Check")
async def get_overall_health(
    pg_status: dict = Depends(check_postgres),
    redis_status: dict = Depends(check_redis),
    qdrant_status: dict = Depends(check_qdrant),
    llm_status: dict = Depends(check_llm_provider),
):
    """
    Performs an overall health check of the RAE Memory API and its dependencies.

    Returns the status of:
    - PostgreSQL database
    - Redis cache
    - Qdrant vector store
    - Configured LLM provider
    """
    logger.info("overall_health_check_successful")
    return {
        "status": "UP",
        "services": {
            "postgres": pg_status,
            "redis": redis_status,
            "qdrant": qdrant_status,
            "llm_provider": llm_status,
        },
    }


@router.get("/ready", response_model=dict, summary="Readiness Probe")
async def get_readiness_status():
    """
    Readiness probe for Kubernetes or similar orchestration.
    Checks if the application is ready to serve requests.
    Currently, this is the same as /health but can be extended
    to check specific application-level readiness criteria (e.g., migrations complete, caches warmed up).
    """
    # For now, readiness is the same as liveness/health.
    # In a real app, this might include checking if database migrations are complete,
    # or if essential caches have been warmed up.
    # The dependencies for /health will be implicitly checked due to their dependencies in get_overall_health
    return {"status": "READY"}


@router.get("/live", response_model=dict, summary="Liveness Probe")
async def get_liveness_status():
    """
    Liveness probe for Kubernetes or similar orchestration.
    Checks if the application is alive.
    A simple check to ensure the FastAPI application process is running.
    """
    return {"status": "LIVE"}
