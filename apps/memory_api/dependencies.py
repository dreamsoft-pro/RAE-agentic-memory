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

from fastapi import Security, HTTPException, Request
from fastapi.security import APIKeyHeader
import asyncpg
from typing import AsyncGenerator

from .config import settings
from .repositories.memory_repository import MemoryRepository
from .repositories.graph_repository import GraphRepository
from .services.graph_extraction import GraphExtractionService
from .services.hybrid_search import HybridSearchService

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# ==========================================
# Authentication Dependencies
# ==========================================

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency to validate the API key provided in the X-API-Key header.
    If settings.API_KEY is not set, authentication is effectively disabled.
    """
    if settings.API_KEY:  # Only enforce if an API_KEY is configured
        if api_key and api_key == settings.API_KEY:
            return api_key
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )
    return None  # Authentication disabled


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
        raise HTTPException(
            status_code=500,
            detail="Database pool not available"
        )
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
        raise HTTPException(
            status_code=500,
            detail="Database pool not available"
        )
    return GraphRepository(pool)


# ==========================================
# Service Layer Dependencies
# ==========================================

def get_graph_extraction_service(
    request: Request
) -> GraphExtractionService:
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

    # Instantiate repositories
    memory_repo = get_memory_repository(pool)
    graph_repo = get_graph_repository(pool)

    # Inject repositories into service
    return GraphExtractionService(
        memory_repo=memory_repo,
        graph_repo=graph_repo
    )


def get_hybrid_search_service(
    request: Request
) -> HybridSearchService:
    """
    Factory for HybridSearchService with full dependency injection.

    This is the Composition Root for hybrid search operations.
    All dependencies are resolved and injected here.

    Args:
        request: FastAPI request object

    Returns:
        Fully configured HybridSearchService instance
    """
    pool = get_db_pool(request)

    # Instantiate repository
    graph_repo = get_graph_repository(pool)

    # Inject dependencies into service
    return HybridSearchService(
        graph_repo=graph_repo,
        pool=pool  # Still needed for vector store
    )
