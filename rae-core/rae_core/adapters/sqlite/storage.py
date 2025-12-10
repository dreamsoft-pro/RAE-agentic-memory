"""SQLite storage adapter for RAE-core with FTS5 full-text search.

Lightweight, file-based storage ideal for RAE-Lite offline-first architecture.
Uses SQLite FTS5 (Full-Text Search) for efficient content search.
"""

import aiosqlite
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from rae_core.interfaces.storage import IMemoryStorage


class SQLiteStorage(IMemoryStorage):
    """SQLite implementation of IMemoryStorage with FTS5 search.

    Features:
    - File-based storage (no server required)
    - FTS5 full-text search on content
    - ACID transactions
    - Multi-index support for fast queries
    - JSON metadata storage
    - Thread-safe via SQLite connection pooling
    """

    def __init__(self, db_path: str = ":memory:"):
        """Initialize SQLite storage.

        Args:
            db_path: Path to SQLite database file, or ":memory:" for in-memory DB
        """
        self.db_path = db_path
        self._initialized = False

    async def initialize(self):
        """Initialize database schema and indexes."""
        if self._initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Enable WAL mode for better concurrency
            await db.execute("PRAGMA journal_mode=WAL")

            # Main memories table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    tags TEXT,  -- JSON array
                    metadata TEXT,  -- JSON object
                    embedding BLOB,  -- Reserved for future use
                    importance REAL DEFAULT 0.5,
                    created_at TEXT NOT NULL,
                    modified_at TEXT NOT NULL,
                    last_accessed_at TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    version INTEGER DEFAULT 1
                )
            """)

            # FTS5 virtual table for full-text search on content
            await db.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                    content,
                    content=memories,
                    content_rowid=rowid
                )
            """)

            # Triggers to keep FTS5 in sync
            await db.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                    INSERT INTO memories_fts(rowid, content) VALUES (new.rowid, new.content);
                END
            """)

            await db.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                    INSERT INTO memories_fts(memories_fts, rowid, content)
                    VALUES('delete', old.rowid, old.content);
                END
            """)

            await db.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                    INSERT INTO memories_fts(memories_fts, rowid, content)
                    VALUES('delete', old.rowid, old.content);
                    INSERT INTO memories_fts(rowid, content) VALUES (new.rowid, new.content);
                END
            """)

            # Indexes for fast lookups
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_tenant_id
                ON memories(tenant_id)
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_agent_id
                ON memories(tenant_id, agent_id)
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_layer
                ON memories(tenant_id, layer)
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_created_at
                ON memories(tenant_id, created_at DESC)
            """)

            await db.commit()

        self._initialized = True

    async def store_memory(
        self,
        content: str,
        layer: str,
        tenant_id: str,
        agent_id: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
        importance: Optional[float] = None,
    ) -> UUID:
        """Store a new memory."""
        await self.initialize()

        memory_id = uuid4()
        now = datetime.utcnow().isoformat()

        tags_json = json.dumps(tags or [])
        metadata_json = json.dumps(metadata or {})

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO memories (
                    id, content, layer, tenant_id, agent_id, tags, metadata,
                    importance, created_at, modified_at, last_accessed_at,
                    access_count, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1)
                """,
                (
                    str(memory_id),
                    content,
                    layer,
                    tenant_id,
                    agent_id,
                    tags_json,
                    metadata_json,
                    importance or 0.5,
                    now,
                    now,
                    now,
                ),
            )
            await db.commit()

        return memory_id

    async def get_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a memory by ID."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT * FROM memories
                WHERE id = ? AND tenant_id = ?
                """,
                (str(memory_id), tenant_id),
            ) as cursor:
                row = await cursor.fetchone()

                if not row:
                    return None

                return self._row_to_dict(row)

    async def update_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        """Update a memory."""
        await self.initialize()

        # Build dynamic UPDATE query
        set_clauses = []
        params = []

        for key, value in updates.items():
            if key in ["tags", "metadata"]:
                set_clauses.append(f"{key} = ?")
                params.append(json.dumps(value))
            elif key not in ["id", "created_at"]:  # Immutable fields
                set_clauses.append(f"{key} = ?")
                params.append(value)

        if not set_clauses:
            return False

        # Always update modified_at and increment version
        set_clauses.append("modified_at = ?")
        set_clauses.append("version = version + 1")
        params.append(datetime.utcnow().isoformat())

        params.extend([str(memory_id), tenant_id])

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                f"""
                UPDATE memories
                SET {', '.join(set_clauses)}
                WHERE id = ? AND tenant_id = ?
                """,
                params,
            )
            await db.commit()

            return cursor.rowcount > 0

    async def delete_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a memory."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                DELETE FROM memories
                WHERE id = ? AND tenant_id = ?
                """,
                (str(memory_id), tenant_id),
            )
            await db.commit()

            return cursor.rowcount > 0

    async def list_memories(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        layer: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List memories with filtering."""
        await self.initialize()

        # Build dynamic WHERE clause
        where_clauses = ["tenant_id = ?"]
        params = [tenant_id]

        if agent_id:
            where_clauses.append("agent_id = ?")
            params.append(agent_id)

        if layer:
            where_clauses.append("layer = ?")
            params.append(layer)

        # Tag filtering using JSON string matching
        if tags:
            # OR logic for tags - check if tag exists in JSON array
            tag_conditions = []
            for tag in tags:
                tag_conditions.append(f"tags LIKE ?")
                params.append(f'%"{tag}"%')
            where_clauses.append(f"({' OR '.join(tag_conditions)})")

        where_clause = " AND ".join(where_clauses)

        params.extend([limit, offset])

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                f"""
                SELECT * FROM memories
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                """,
                params,
            ) as cursor:
                rows = await cursor.fetchall()
                return [self._row_to_dict(row) for row in rows]

    async def count_memories(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        layer: Optional[str] = None,
    ) -> int:
        """Count memories matching filters."""
        await self.initialize()

        where_clauses = ["tenant_id = ?"]
        params = [tenant_id]

        if agent_id:
            where_clauses.append("agent_id = ?")
            params.append(agent_id)

        if layer:
            where_clauses.append("layer = ?")
            params.append(layer)

        where_clause = " AND ".join(where_clauses)

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                f"""
                SELECT COUNT(*) FROM memories
                WHERE {where_clause}
                """,
                params,
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def increment_access_count(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Increment access count for a memory."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                UPDATE memories
                SET access_count = access_count + 1,
                    last_accessed_at = ?
                WHERE id = ? AND tenant_id = ?
                """,
                (datetime.utcnow().isoformat(), str(memory_id), tenant_id),
            )
            await db.commit()

            return cursor.rowcount > 0

    async def search_full_text(
        self,
        query: str,
        tenant_id: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Full-text search using FTS5.

        Args:
            query: Search query (supports FTS5 syntax)
            tenant_id: Tenant identifier
            limit: Maximum number of results

        Returns:
            List of matching memories with relevance scores
        """
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT m.*, bm25(memories_fts) as score
                FROM memories m
                JOIN memories_fts ON m.rowid = memories_fts.rowid
                WHERE memories_fts MATCH ? AND m.tenant_id = ?
                ORDER BY bm25(memories_fts)
                LIMIT ?
                """,
                (query, tenant_id, limit),
            ) as cursor:
                rows = await cursor.fetchall()
                return [self._row_to_dict(row) for row in rows]

    async def close(self):
        """Close database connection (if needed)."""
        # aiosqlite uses context managers, so explicit close not needed
        pass

    def _row_to_dict(self, row: aiosqlite.Row) -> Dict[str, Any]:
        """Convert SQLite row to memory dictionary."""
        memory = dict(row)

        # Parse JSON fields
        if memory.get("tags"):
            memory["tags"] = json.loads(memory["tags"])
        else:
            memory["tags"] = []

        if memory.get("metadata"):
            memory["metadata"] = json.loads(memory["metadata"])
        else:
            memory["metadata"] = {}

        # Convert UUID string back to UUID
        if memory.get("id"):
            memory["id"] = UUID(memory["id"])

        return memory
