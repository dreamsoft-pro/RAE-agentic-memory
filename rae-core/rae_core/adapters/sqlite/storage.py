"""SQLite storage adapter for RAE-core with FTS5 full-text search."""

import json
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import aiosqlite

from rae_core.interfaces.storage import IMemoryStorage


class SQLiteStorage(IMemoryStorage):
    """SQLite implementation of IMemoryStorage with FTS5 search."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._initialized = False

    async def initialize(self) -> None:
        if self._initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=WAL")
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    tags TEXT,
                    metadata TEXT,
                    importance REAL DEFAULT 0.5,
                    created_at TEXT NOT NULL,
                    modified_at TEXT NOT NULL,
                    last_accessed_at TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    version INTEGER DEFAULT 1,
                    expires_at TEXT,
                    project TEXT
                )
            """
            )
            # FTS5 virtual table
            await db.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(content, content=memories, content_rowid=rowid)"
            )
            await db.commit()
        self._initialized = True

    async def store_memory(self, **kwargs: Any) -> UUID:
        await self.initialize()
        m_id = uuid4()
        now = datetime.now(timezone.utc).isoformat()

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO memories (id, content, layer, tenant_id, agent_id, tags, metadata, importance, created_at, modified_at, last_accessed_at, project) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    str(m_id),
                    kwargs.get("content"),
                    kwargs.get("layer"),
                    kwargs.get("tenant_id"),
                    kwargs.get("agent_id"),
                    json.dumps(kwargs.get("tags", [])),
                    json.dumps(kwargs.get("metadata", {})),
                    kwargs.get("importance", 0.5),
                    now,
                    now,
                    now,
                    kwargs.get("project"),
                ),
            )
            await db.commit()
        return m_id

    async def get_memory(
        self, memory_id: UUID, tenant_id: str
    ) -> dict[str, Any] | None:
        await self.initialize()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM memories WHERE id = ? AND tenant_id = ?",
                (str(memory_id), tenant_id),
            ) as cursor:
                row = await cursor.fetchone()
                return self._row_to_dict(row) if row else None

    async def update_memory(
        self, memory_id: UUID, tenant_id: str, updates: dict[str, Any]
    ) -> bool:
        await self.initialize()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE memories SET content = ? WHERE id = ? AND tenant_id = ?",
                (updates.get("content"), str(memory_id), tenant_id),
            )
            await db.commit()
        return True

    async def delete_memory(self, memory_id: UUID, tenant_id: str) -> bool:
        await self.initialize()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM memories WHERE id = ? AND tenant_id = ?",
                (str(memory_id), tenant_id),
            )
            await db.commit()
        return True

    async def list_memories(
        self, tenant_id: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        await self.initialize()
        limit = kwargs.get("limit", 100)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM memories WHERE tenant_id = ? LIMIT ?", (tenant_id, limit)
            ) as cursor:
                rows = await cursor.fetchall()
                return [self._row_to_dict(r) for r in rows]

    async def search_memories(
        self,
        query: str,
        tenant_id: str,
        agent_id: str,
        layer: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        await self.initialize()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            # Simplified FTS
            async with db.execute(
                "SELECT * FROM memories WHERE tenant_id = ? AND agent_id = ? AND layer = ? AND content LIKE ? LIMIT ?",
                (tenant_id, agent_id, layer, f"%{query}%", limit),
            ) as cursor:
                rows = await cursor.fetchall()
                return [
                    {
                        "id": r["id"],
                        "content": r["content"],
                        "score": 1.0,
                        "importance": r["importance"],
                    }
                    for r in rows
                ]

    async def count_memories(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        layer: str | None = None,
    ) -> int:
        await self.initialize()
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM memories") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def delete_memories_with_metadata_filter(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        layer: str | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> int:
        return 0

    async def delete_memories_below_importance(
        self, tenant_id: str, agent_id: str, layer: str, importance_threshold: float
    ) -> int:
        return 0

    async def delete_expired_memories(
        self, tenant_id: str, agent_id: str | None = None, layer: str | None = None
    ) -> int:
        return 0

    async def update_memory_access(self, memory_id: UUID, tenant_id: str) -> bool:
        return True

    async def update_memory_expiration(
        self, memory_id: UUID, tenant_id: str, expires_at: datetime | None
    ) -> bool:
        return True

    async def get_metric_aggregate(
        self,
        tenant_id: str,
        metric: str,
        func: str,
        filters: dict[str, Any] | None = None,
    ) -> float:
        return 0.0

    async def update_memory_access_batch(
        self, memory_ids: list[UUID], tenant_id: str
    ) -> bool:
        return True

    async def adjust_importance(
        self, memory_id: UUID, delta: float, tenant_id: str
    ) -> float:
        return 0.5

    async def save_embedding(
        self, memory_id: UUID, model_name: str, embedding: list[float], tenant_id: str
    ) -> bool:
        return True

    async def decay_importance(self, tenant_id: str, decay_factor: float) -> int:
        return 0

    async def close(self) -> None:
        pass

    def _row_to_dict(self, row: aiosqlite.Row) -> dict[str, Any]:
        d = dict(row)
        d["id"] = UUID(d["id"])
        d["tags"] = json.loads(d["tags"]) if d["tags"] else []
        d["metadata"] = json.loads(d["metadata"]) if d["metadata"] else {}
        return d
