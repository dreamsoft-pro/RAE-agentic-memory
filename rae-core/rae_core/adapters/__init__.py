"""Storage and service adapters for RAE-core.

This module provides concrete implementations of the abstract interfaces:
- PostgreSQLStorage: IMemoryStorage implementation using asyncpg
- QdrantVectorStore: IVectorStore implementation using Qdrant
- RedisCache: ICacheProvider implementation using Redis

Adapters follow dependency injection pattern for easy testing and swapping.
"""

from .postgres import PostgreSQLStorage
from .qdrant import QdrantVectorStore
from .redis import RedisCache

__all__ = [
    "PostgreSQLStorage",
    "QdrantVectorStore",
    "RedisCache",
]
