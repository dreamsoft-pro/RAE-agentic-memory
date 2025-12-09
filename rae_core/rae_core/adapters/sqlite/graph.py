"""
SQLite Graph Store Adapter.

Implements graph storage using SQLite for nodes and edges.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

import aiosqlite


class SQLiteGraphStore:
    """
    SQLite-based graph storage.

    Features:
    - Nodes and edges tables
    - Adjacency list queries
    - Breadth-first search for neighbors
    - JSON properties storage
    """

    def __init__(self, db_path: str = "rae_graph.db"):
        """
        Initialize graph store.

        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._initialized = False

    async def initialize(self) -> None:
        """Create tables if they don't exist."""
        if self._initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Nodes table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    label TEXT NOT NULL,
                    tenant_id TEXT,
                    project TEXT,
                    properties TEXT,
                    created_at TEXT NOT NULL
                )
            """
            )

            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_nodes_tenant_project ON nodes(tenant_id, project)"
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_nodes_label ON nodes(label)"
            )

            # Edges table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS edges (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    tenant_id TEXT,
                    project TEXT,
                    properties TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES nodes(id) ON DELETE CASCADE,
                    FOREIGN KEY (target_id) REFERENCES nodes(id) ON DELETE CASCADE
                )
            """
            )

            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id)"
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id)"
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_edges_relation ON edges(relation)"
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_edges_tenant_project ON edges(tenant_id, project)"
            )

            await db.commit()

        self._initialized = True

    async def add_node(
        self,
        node_id: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a node to the graph."""
        await self.initialize()

        now = datetime.utcnow().isoformat()
        properties_json = json.dumps(properties) if properties else "{}"

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT OR REPLACE INTO nodes
                (id, label, tenant_id, project, properties, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (node_id, label, tenant_id, project, properties_json, now),
            )
            await db.commit()

        return {
            "id": node_id,
            "label": label,
            "properties": properties or {},
            "created_at": now,
        }

    async def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        properties: Optional[Dict[str, Any]] = None,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add an edge between two nodes."""
        await self.initialize()

        edge_id = f"edge_{uuid4().hex[:12]}"
        now = datetime.utcnow().isoformat()
        properties_json = json.dumps(properties) if properties else "{}"

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO edges
                (id, source_id, target_id, relation, tenant_id, project, properties, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    edge_id,
                    source_id,
                    target_id,
                    relation,
                    tenant_id,
                    project,
                    properties_json,
                    now,
                ),
            )
            await db.commit()

        return {
            "id": edge_id,
            "source_id": source_id,
            "target_id": target_id,
            "relation": relation,
            "properties": properties or {},
            "created_at": now,
        }

    async def get_node(
        self,
        node_id: str,
        tenant_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Get a node by ID."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            query = "SELECT * FROM nodes WHERE id = ?"
            params = [node_id]

            if tenant_id:
                query += " AND tenant_id = ?"
                params.append(tenant_id)

            async with db.execute(query, params) as cursor:
                row = await cursor.fetchone()

            if not row:
                return None

            return self._node_row_to_dict(row)

    async def get_neighbors(
        self,
        node_id: str,
        depth: int = 1,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get neighboring nodes up to specified depth."""
        await self.initialize()

        if depth < 1:
            return []

        visited = set()
        current_level = {node_id}
        all_neighbors = []

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            for _ in range(depth):
                if not current_level:
                    break

                next_level = set()

                for current_id in current_level:
                    if current_id in visited:
                        continue

                    visited.add(current_id)

                    # Find outgoing edges
                    query = """
                        SELECT n.*, e.relation, e.id as edge_id
                        FROM edges e
                        JOIN nodes n ON e.target_id = n.id
                        WHERE e.source_id = ?
                    """
                    params = [current_id]

                    if tenant_id:
                        query += " AND e.tenant_id = ?"
                        params.append(tenant_id)

                    if project:
                        query += " AND e.project = ?"
                        params.append(project)

                    async with db.execute(query, params) as cursor:
                        rows = await cursor.fetchall()

                    for row in rows:
                        neighbor = self._node_row_to_dict(row)
                        neighbor["edge_relation"] = row["relation"]
                        neighbor["edge_id"] = row["edge_id"]
                        all_neighbors.append(neighbor)
                        next_level.add(neighbor["id"])

                current_level = next_level

        return all_neighbors

    async def delete_node(
        self,
        node_id: str,
        tenant_id: Optional[str] = None,
    ) -> bool:
        """Delete a node and its edges."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            # Delete edges
            await db.execute(
                "DELETE FROM edges WHERE source_id = ? OR target_id = ?",
                (node_id, node_id),
            )

            # Delete node
            query = "DELETE FROM nodes WHERE id = ?"
            params = [node_id]

            if tenant_id:
                query += " AND tenant_id = ?"
                params.append(tenant_id)

            cursor = await db.execute(query, params)
            await db.commit()

            return cursor.rowcount > 0

    async def delete_edge(
        self,
        edge_id: str,
        tenant_id: Optional[str] = None,
    ) -> bool:
        """Delete an edge."""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            query = "DELETE FROM edges WHERE id = ?"
            params = [edge_id]

            if tenant_id:
                query += " AND tenant_id = ?"
                params.append(tenant_id)

            cursor = await db.execute(query, params)
            await db.commit()

            return cursor.rowcount > 0

    async def query_nodes(
        self,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None,
        label: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query nodes with filters."""
        await self.initialize()

        conditions = []
        params = []

        if tenant_id:
            conditions.append("tenant_id = ?")
            params.append(tenant_id)

        if project:
            conditions.append("project = ?")
            params.append(project)

        if label:
            conditions.append("label = ?")
            params.append(label)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        params.append(limit)

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            query = f"""
                SELECT * FROM nodes
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT ?
            """

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()

            return [self._node_row_to_dict(row) for row in rows]

    def _node_row_to_dict(self, row: aiosqlite.Row) -> Dict[str, Any]:
        """Convert node row to dictionary."""
        data = dict(row)

        # Parse properties JSON
        if data.get("properties"):
            try:
                data["properties"] = json.loads(data["properties"])
            except (json.JSONDecodeError, TypeError):
                data["properties"] = {}

        return data

    async def close(self) -> None:
        """Close database connection."""
        pass
