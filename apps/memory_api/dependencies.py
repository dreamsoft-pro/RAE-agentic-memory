"""
Dependency Injection Configuration for RAE Memory API.

This module implements the Composition Root pattern, providing factory functions
for FastAPI dependency injection. All service dependencies are resolved here,
ensuring clean separation of concerns and testability.

Enterprise Architecture Benefits:
- Single source of truth for dependency wiring
- Easy mocking and testing (inject test repositories)
- Clear dependency graph
- No hidden dependencies
"""

import asyncpg
import redis.asyncio as aioredis
from fastapi import HTTPException, Request
from qdrant_client import QdrantClient
from redis.asyncio import Redis as AsyncRedis

from .repositories.graph_repository import GraphRepository
from .repositories.memory_repository import MemoryRepository
from .services.graph_extraction import GraphExtractionService
from .services.hybrid_search import HybridSearchService
from .services.rae_core_service import RAECoreService

# ==========================================
# Authentication Dependencies
# ==========================================
# NOTE: Auth dependencies moved to apps/memory_api/security/auth.py
# Use verify_token() for authentication globally via FastAPI dependencies
# or import from security.auth for specific endpoints


# ==========================================
# Database Connection Pool
# ==========================================


def get_db_pool(request: Request) -> asyncpg.Pool:
    """
    Get the database connection pool from application state.

    Args:
        request: FastAPI request object

    Returns:
        AsyncPG connection pool
    """
    return request.app.state.pool


# ==========================================
# External Services Clients
# ==========================================


async def create_redis_client(redis_url: str) -> AsyncRedis:
    """
    Factory function to create an asynchronous Redis client.
    """
    return aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)


def get_redis_client(request: Request) -> AsyncRedis:
    """
    Get the Redis client from application state.
    """
    if not hasattr(request.app.state, "redis_client"):
        raise HTTPException(status_code=500, detail="Redis client not initialized")
    return request.app.state.redis_client


def get_qdrant_client(request: Request) -> QdrantClient:
    """
    Get the Qdrant client from application state.
    """
    if not hasattr(request.app.state, "qdrant_client"):
        raise HTTPException(status_code=500, detail="Qdrant client not initialized")
    return request.app.state.qdrant_client


# ==========================================
# Repository Layer Dependencies
# ==========================================


def get_memory_repository(pool: asyncpg.Pool = None) -> MemoryRepository:
    """
    Factory for MemoryRepository.

    Args:
        pool: Database connection pool (injected by FastAPI)

    Returns:
        Configured MemoryRepository instance
    """
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not available")
    return MemoryRepository(pool)


def get_graph_repository(pool: asyncpg.Pool = None) -> GraphRepository:
    """
    Factory for GraphRepository.

    Args:
        pool: Database connection pool (injected by FastAPI)

    Returns:
        Configured GraphRepository instance
    """
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not available")
    return GraphRepository(pool)


# ==========================================
# Service Layer Dependencies
# ==========================================


def get_rae_core_service(request: Request) -> RAECoreService:
    """
    Factory for RAECoreService with full dependency injection.

    Composition root for RAE-Core integration.
    Provides access to RAEEngine and storage adapters.

    Args:
        request: FastAPI request object

    Returns:
        Fully configured RAECoreService instance
    """
    if not hasattr(request.app.state, "rae_core_service"):
        raise HTTPException(status_code=500, detail="RAE-Core service not initialized")
    return request.app.state.rae_core_service


def get_graph_extraction_service(request: Request) -> GraphExtractionService:
    """
    Factory for GraphExtractionService with full dependency injection.

    This is the Composition Root for graph extraction operations.
    All dependencies are resolved and injected here.

    Args:
        request: FastAPI request object

    Returns:
        Fully configured GraphExtractionService instance
    """
    pool = get_db_pool(request)
    rae_service = get_rae_core_service(request)

    # Instantiate repositories
    # memory_repo = get_memory_repository(pool) # Deprecated
    graph_repo = get_graph_repository(pool)

    # Inject repositories into service
    return GraphExtractionService(rae_service=rae_service, graph_repo=graph_repo)
