"""Storage and service adapters for RAE-core.

This module provides concrete implementations of the abstract interfaces:
- PostgreSQLStorage: IMemoryStorage implementation using asyncpg
- QdrantVectorStore: IVectorStore implementation using Qdrant
- RedisCache: ICacheProvider implementation using Redis
- SQLiteStorage: IMemoryStorage implementation using SQLite
- SQLiteVectorStore: IVectorStore implementation using SQLite
- InMemoryStorage: IMemoryStorage for testing
- InMemoryVectorStore: IVectorStore for testing
- InMemoryCache: ICacheProvider for testing

Adapters follow dependency injection pattern for easy testing and swapping.
"""

from .memory.cache import InMemoryCache
from .memory.storage import InMemoryStorage
from .memory.vector import InMemoryVectorStore
from .postgres_adapter import PostgreSQLStorage
from .qdrant_adapter import QdrantVectorStore
from .redis_adapter import RedisAdapter as RedisCache
from .sqlite.storage import SQLiteStorage
from .sqlite.vector import SQLiteVectorStore

# Aliases for backwards compatibility
PostgresMemoryAdapter = PostgreSQLStorage
QdrantVectorAdapter = QdrantVectorStore
RedisCacheAdapter = RedisCache

__all__ = [
    "PostgreSQLStorage",
    "QdrantVectorStore",
    "RedisCache",
    "SQLiteStorage",
    "SQLiteVectorStore",
    "InMemoryStorage",
    "InMemoryVectorStore",
    "InMemoryCache",
    # Aliases
    "PostgresMemoryAdapter",
    "QdrantVectorAdapter",
    "RedisCacheAdapter",
]
