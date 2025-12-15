"""Abstract cache provider interface for RAE-core."""

from abc import ABC, abstractmethod
from typing import Any


class ICacheProvider(ABC):
    """Abstract interface for cache providers (Redis, in-memory, etc.)."""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        """Set value in cache with optional TTL in seconds."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass

    @abstractmethod
    async def clear(self, pattern: str | None = None) -> int:
        """Clear cache keys matching pattern (all if None)."""
        pass
