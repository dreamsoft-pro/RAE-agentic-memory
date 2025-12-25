"""Abstract database provider interface for RAE-core.

Allows RAE to run on different database backends (PostgreSQL, SQLite, etc.)
while keeping high-level logic (like graph operations) agnostic.
"""

from abc import ABC, abstractmethod
from typing import Any


class IDatabaseProvider(ABC):
    """Abstract interface for low-level database operations."""

    @abstractmethod
    async def fetchrow(self, query: str, *args: Any) -> dict[str, Any] | None:
        """Fetch a single row from the database."""
        pass

    @abstractmethod
    async def fetch(self, query: str, *args: Any) -> list[dict[str, Any]]:
        """Fetch multiple rows from the database."""
        pass

    @abstractmethod
    async def fetchval(self, query: str, *args: Any) -> Any:
        """Fetch a single value from the database."""
        pass

    @abstractmethod
    async def execute(self, query: str, *args: Any) -> str:
        """Execute a command (INSERT, UPDATE, DELETE)."""
        pass

    @abstractmethod
    def acquire(self) -> Any:
        """Acquire a connection from the pool."""
        pass
