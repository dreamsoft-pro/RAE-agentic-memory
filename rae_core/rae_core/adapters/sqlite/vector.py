"""
SQLite Vector Store Adapter.

Implements vector storage using SQLite + numpy for similarity search.
Optionally uses sqlite-vec extension if available.
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

import aiosqlite
import numpy as np


class SQLiteVectorStore:
    """
    SQLite-based vector storage with numpy similarity search.

    Features:
    - Stores vectors as JSON (or BLOB)
    - Numpy-based cosine similarity
    - Optional sqlite-vec extension support
    - Automatic table creation
    """

    def __init__(
        self,
        db_path: str = "rae_vectors.db",
        use_sqlite_vec: bool = False,
        dimension: int = 1536,
    ):
        """
        Initialize vector store.

        Args:
            db_path: Path to SQLite database
            use_sqlite_vec: Whether to try using sqlite-vec extension
            dimension: Vector dimension (default: OpenAI ada-002)
        """
        self.db_path = db_path
        self.use_sqlite_vec = use_sqlite_vec
        self.dimension = dimension
        self._initialized = False
        self._has_sqlite_vec = False

    async def initialize(self) -> None:
        """Create tables and check for sqlite-vec extension."""
        if self._initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Check for sqlite-vec extension
            if self.use_sqlite_vec:
                try:
                    await db.enable_load_extension(True)
                    await db.execute("SELECT load_extension('vec0')")
                    self._has_sqlite_vec = True
                except (sqlite3.OperationalError, aiosqlite.Error):
                    self._has_sqlite_vec = False

            if self._has_sqlite_vec:
                # Use sqlite-vec table
                await db.execute(
                    f"""
                    CREATE VIRTUAL TABLE IF NOT EXISTS vectors USING vec0(
                        id TEXT PRIMARY KEY,
                        embedding float[{self.dimension}]
                    )
                """
                )
            else:
                # Use regular table with JSON vectors
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS vectors (
                        id TEXT PRIMARY KEY,
                        tenant_id TEXT NOT NULL,
                        project TEXT NOT NULL,
                        content TEXT,
                        embedding TEXT NOT NULL,
                        metadata TEXT,
                        created_at TEXT NOT NULL
                    )
                """
                )

                await db.execute(
                    "CREATE INDEX IF NOT EXISTS idx_vectors_tenant_project ON vectors(tenant_id, project)"
                )

            await db.commit()

        self._initialized = True

    async def upsert_vector(
        self,
        vector_id: str,
        embedding: List[float],
        tenant_id: str,
        project: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Insert or update a vector."""
        await self.initialize()

        from datetime import datetime

        now = datetime.utcnow().isoformat()
        embedding_json = json.dumps(embedding)
        metadata_json = json.dumps(metadata) if metadata else "{}"

        async with aiosqlite.connect(self.db_path) as db:
            if self._has_sqlite_vec:
                # sqlite-vec format
                await db.execute(
                    "INSERT OR REPLACE INTO vectors (id, embedding) VALUES (?, ?)",
                    (vector_id, embedding_json),
                )
            else:
                # Regular SQLite
                await db.execute(
                    """
                    INSERT OR REPLACE INTO vectors
                    (id, tenant_id, project, content, embedding, metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        vector_id,
                        tenant_id,
                        project,
                        content,
                        embedding_json,
                        metadata_json,
                        now,
                    ),
                )

            await db.commit()

    async def search_similar(
        self,
        query_embedding: List[float],
        tenant_id: str,
        project: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float]]:
        """
        Search for similar vectors.

        Returns:
            List of (vector_id, similarity_score) tuples
        """
        await self.initialize()

        if self._has_sqlite_vec:
            return await self._search_with_sqlite_vec(
                query_embedding, tenant_id, project, k, filters
            )
        else:
            return await self._search_with_numpy(
                query_embedding, tenant_id, project, k, filters
            )

    async def _search_with_sqlite_vec(
        self,
        query_embedding: List[float],
        tenant_id: str,
        project: str,
        k: int,
        filters: Optional[Dict[str, Any]],
    ) -> List[Tuple[str, float]]:
        """Search using sqlite-vec extension."""
        async with aiosqlite.connect(self.db_path) as db:
            query_json = json.dumps(query_embedding)

            async with db.execute(
                f"""
                SELECT id, distance
                FROM vectors
                WHERE embedding MATCH ?
                  AND k = ?
                ORDER BY distance
                LIMIT ?
            """,
                (query_json, k, k),
            ) as cursor:
                rows = await cursor.fetchall()

            return [(row[0], 1.0 - row[1]) for row in rows]  # Convert distance to similarity

    async def _search_with_numpy(
        self,
        query_embedding: List[float],
        tenant_id: str,
        project: str,
        k: int,
        filters: Optional[Dict[str, Any]],
    ) -> List[Tuple[str, float]]:
        """Search using numpy cosine similarity."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Fetch all vectors for tenant/project
            query = "SELECT id, embedding FROM vectors WHERE tenant_id = ? AND project = ?"
            params = [tenant_id, project]

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()

            if not rows:
                return []

            # Calculate similarities
            query_vec = np.array(query_embedding, dtype=np.float32)
            query_vec = query_vec / np.linalg.norm(query_vec)  # Normalize

            results = []
            for row in rows:
                try:
                    embedding = json.loads(row["embedding"])
                    vec = np.array(embedding, dtype=np.float32)
                    vec = vec / np.linalg.norm(vec)  # Normalize

                    # Cosine similarity
                    similarity = float(np.dot(query_vec, vec))
                    results.append((row["id"], similarity))
                except (json.JSONDecodeError, ValueError, ZeroDivisionError):
                    continue

            # Sort by similarity and return top k
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:k]

    async def get_vector(self, vector_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a vector by ID."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            async with db.execute(
                "SELECT * FROM vectors WHERE id = ?", (vector_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                return None

            data = dict(row)

            # Parse JSON fields
            if data.get("embedding"):
                try:
                    data["embedding"] = json.loads(data["embedding"])
                except (json.JSONDecodeError, TypeError):
                    data["embedding"] = []

            if data.get("metadata"):
                try:
                    data["metadata"] = json.loads(data["metadata"])
                except (json.JSONDecodeError, TypeError):
                    data["metadata"] = {}

            return data

    async def delete_vector(self, vector_id: str) -> bool:
        """Delete a vector by ID."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM vectors WHERE id = ?", (vector_id,))
            await db.commit()
            return cursor.rowcount > 0

    async def count_vectors(self, tenant_id: str, project: str) -> int:
        """Count total vectors for a tenant/project."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT COUNT(*) FROM vectors WHERE tenant_id = ? AND project = ?",
                (tenant_id, project),
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def close(self) -> None:
        """Close database connection."""
        pass
