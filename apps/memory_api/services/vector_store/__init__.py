from functools import lru_cache
from .base import MemoryVectorStore
from .qdrant_store import QdrantStore
from .pgvector_store import PGVectorStore
from ...config import settings
import asyncpg # Required for PGVectorStore

@lru_cache(maxsize=1)
def get_vector_store(pool: asyncpg.Pool = None) -> MemoryVectorStore:
    """
    Factory function to get the configured vector store provider.
    Uses a singleton pattern to ensure only one provider instance is created.
    """
    backend = settings.RAE_VECTOR_BACKEND

    if backend == "qdrant":
        return QdrantStore()
    elif backend == "pgvector":
        if not pool:
            raise ValueError("An asyncpg connection pool is required for the PGVector backend.")
        return PGVectorStore(pool)
    else:
        raise ValueError(f"Unknown vector store backend specified: {backend}")
