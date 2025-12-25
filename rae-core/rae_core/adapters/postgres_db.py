"""PostgreSQL implementation of IDatabaseProvider."""

from typing import Any, cast

import asyncpg

from rae_core.interfaces.database import IDatabaseProvider


class PostgresDatabaseProvider(IDatabaseProvider):
    """Database provider using asyncpg for PostgreSQL."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def fetchrow(self, query: str, *args: Any) -> dict[str, Any] | None:
        record = await self.pool.fetchrow(query, *args)
        return dict(record) if record else None

    async def fetch(self, query: str, *args: Any) -> list[dict[str, Any]]:
        records = await self.pool.fetch(query, *args)
        return [dict(r) for r in records]

    async def fetchval(self, query: str, *args: Any) -> Any:
        return await self.pool.fetchval(query, *args)

    async def execute(self, query: str, *args: Any) -> str:
        return cast(str, await self.pool.execute(query, *args))

    async def executemany(self, query: str, args: list[Any]) -> str:
        return cast(str, await self.pool.executemany(query, args))

    def acquire(self) -> Any:
        return self.pool.acquire()
