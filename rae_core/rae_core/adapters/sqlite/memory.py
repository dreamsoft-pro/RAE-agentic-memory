"""
SQLite Memory Storage Adapter.

Implements MemoryRepositoryProtocol using SQLite for local-first storage.
"""

import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

import aiosqlite


class SQLiteMemoryStorage:
    """
    SQLite implementation of memory storage.

    Features:
    - Async operations via aiosqlite
    - JSON storage for metadata and tags
    - Full-text search (FTS5)
    - Automatic schema creation
    """

    def __init__(self, db_path: str = "rae_memory.db"):
        """
        Initialize SQLite storage.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._initialized = False

    async def initialize(self) -> None:
        """Create tables if they don't exist."""
        if self._initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Main memories table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL,
                    project TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    importance REAL NOT NULL DEFAULT 0.5,
                    layer TEXT,
                    tags TEXT,
                    metadata TEXT,
                    created_at TEXT NOT NULL,
                    last_accessed_at TEXT,
                    usage_count INTEGER DEFAULT 0,
                    timestamp TEXT
                )
            """
            )

            # Indexes for common queries
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_tenant_project ON memories(tenant_id, project)"
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_layer ON memories(layer)"
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC)"
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at DESC)"
            )

            # FTS5 virtual table for full-text search
            await db.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                    memory_id UNINDEXED,
                    content,
                    tags,
                    tokenize='porter unicode61'
                )
            """
            )

            await db.commit()

        self._initialized = True

    async def insert_memory(
        self,
        tenant_id: str,
        content: str,
        source: str,
        importance: float,
        layer: Optional[str],
        tags: Optional[List[str]],
        timestamp: Any,
        project: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Insert a new memory."""
        await self.initialize()

        memory_id = f"mem_{uuid4().hex[:12]}"
        now = datetime.utcnow().isoformat()

        tags_json = json.dumps(tags) if tags else "[]"
        metadata_json = json.dumps(metadata) if metadata else "{}"
        timestamp_str = timestamp.isoformat() if timestamp else now

        async with aiosqlite.connect(self.db_path) as db:
            # Insert into main table
            await db.execute(
                """
                INSERT INTO memories (
                    id, tenant_id, project, content, source, importance,
                    layer, tags, metadata, created_at, last_accessed_at,
                    usage_count, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    memory_id,
                    tenant_id,
                    project,
                    content,
                    source,
                    importance,
                    layer,
                    tags_json,
                    metadata_json,
                    now,
                    now,
                    0,
                    timestamp_str,
                ),
            )

            # Insert into FTS table
            tags_text = " ".join(tags) if tags else ""
            await db.execute(
                "INSERT INTO memories_fts (memory_id, content, tags) VALUES (?, ?, ?)",
                (memory_id, content, tags_text),
            )

            await db.commit()

        return {
            "id": memory_id,
            "created_at": now,
            "last_accessed_at": now,
            "usage_count": 0,
        }

    async def get_memory_by_id(
        self, memory_id: str, tenant_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a memory by ID."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM memories WHERE id = ? AND tenant_id = ?",
                (memory_id, tenant_id),
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                return None

            return self._row_to_dict(row)

    async def query_memories(
        self,
        tenant_id: str,
        project: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Query memories with optional filters."""
        await self.initialize()

        filters = filters or {}

        # Build WHERE clause
        conditions = ["tenant_id = ?", "project = ?"]
        params = [tenant_id, project]

        if "layer" in filters:
            conditions.append("layer = ?")
            params.append(filters["layer"])

        if "min_importance" in filters:
            conditions.append("importance >= ?")
            params.append(filters["min_importance"])

        if "query" in filters:
            # Full-text search
            fts_query = filters["query"]
            conditions.append(
                """
                id IN (
                    SELECT memory_id FROM memories_fts
                    WHERE memories_fts MATCH ?
                )
            """
            )
            params.append(fts_query)

        where_clause = " AND ".join(conditions)
        params.append(limit)

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            query = f"""
                SELECT * FROM memories
                WHERE {where_clause}
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            """

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()

            return [self._row_to_dict(row) for row in rows]

    async def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        """Delete a memory by ID."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            # Delete from FTS
            await db.execute(
                "DELETE FROM memories_fts WHERE memory_id = ?", (memory_id,)
            )

            # Delete from main table
            cursor = await db.execute(
                "DELETE FROM memories WHERE id = ? AND tenant_id = ?",
                (memory_id, tenant_id),
            )

            await db.commit()
            return cursor.rowcount > 0

    async def update_memory_access(self, memory_id: str, tenant_id: str) -> None:
        """Update last_accessed_at and increment usage_count."""
        await self.initialize()

        now = datetime.utcnow().isoformat()

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                UPDATE memories
                SET last_accessed_at = ?, usage_count = usage_count + 1
                WHERE id = ? AND tenant_id = ?
            """,
                (now, memory_id, tenant_id),
            )
            await db.commit()

    def _row_to_dict(self, row: aiosqlite.Row) -> Dict[str, Any]:
        """Convert SQLite row to dictionary."""
        data = dict(row)

        # Parse JSON fields
        if data.get("tags"):
            try:
                data["tags"] = json.loads(data["tags"])
            except (json.JSONDecodeError, TypeError):
                data["tags"] = []

        if data.get("metadata"):
            try:
                data["metadata"] = json.loads(data["metadata"])
            except (json.JSONDecodeError, TypeError):
                data["metadata"] = {}

        return data

    async def close(self) -> None:
        """Close the database connection (no-op for aiosqlite)."""
        pass
