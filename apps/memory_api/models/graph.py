"""
Graph Models - Data structures for knowledge graph entities.

These models represent nodes and edges in the knowledge graph,
used by both repositories and services.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum


class TraversalStrategy(str, Enum):
    """Graph traversal strategies."""
    BFS = "bfs"  # Breadth-first search
    DFS = "dfs"  # Depth-first search


class GraphNode(BaseModel):
    """Represents a node in the knowledge graph."""

    id: str
    node_id: str
    label: str
    properties: Optional[Dict[str, Any]] = None
    depth: int = 0  # Distance from start node


class GraphEdge(BaseModel):
    """Represents an edge in the knowledge graph."""

    source_id: str
    target_id: str
    relation: str
    properties: Optional[Dict[str, Any]] = None
