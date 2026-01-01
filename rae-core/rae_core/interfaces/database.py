"""Abstract database provider interface for RAE-core."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class IDatabaseProvider(Protocol):
    """Abstract interface for database providers."""

    async def execute(self, query: str, *args: Any) -> str:
        """Execute a SQL query."""
        ...

    async def fetch(self, query: str, *args: Any) -> list[dict[str, Any]]:
        """Fetch multiple rows from a SQL query."""
        ...

    async def fetchrow(self, query: str, *args: Any) -> dict[str, Any] | None:
        """Fetch a single row from a SQL query."""
        ...

    async def fetchval(self, query: str, *args: Any) -> Any:
        """Fetch a single value from a SQL query."""
        ...

    async def close(self) -> None:
        """Close the database connection."""
        ...
