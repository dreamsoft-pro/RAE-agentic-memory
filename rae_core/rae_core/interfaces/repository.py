"""
Abstract Repository Interfaces for RAE-Core

These protocols define the contract for data access without coupling to specific implementations.
"""

from typing import Any, Dict, List, Optional, Protocol
from uuid import UUID


class MemoryRepositoryProtocol(Protocol):
    """
    Abstract interface for memory storage operations.

    Implementations can use PostgreSQL, SQLite, in-memory, or any other storage.
    """

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
        """Insert a new memory and return its metadata."""
        ...

    async def get_memory_by_id(self, memory_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a memory by its ID."""
        ...

    async def query_memories(
        self,
        tenant_id: str,
        project: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Query memories with optional filters."""
        ...

    async def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        """Delete a memory by ID."""
        ...

    async def update_memory_access(self, memory_id: str, tenant_id: str) -> None:
        """Update last_accessed_at and increment usage_count."""
        ...


class GraphRepositoryProtocol(Protocol):
    """
    Abstract interface for knowledge graph operations.
    """

    async def add_node(
        self,
        node_id: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a node to the graph."""
        ...

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
        ...

    async def get_neighbors(
        self,
        node_id: str,
        depth: int = 1,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get neighboring nodes up to specified depth."""
        ...

    async def delete_node(
        self,
        node_id: str,
        tenant_id: Optional[str] = None,
    ) -> bool:
        """Delete a node and its edges."""
        ...


class ReflectionRepositoryProtocol(Protocol):
    """
    Abstract interface for reflection storage operations.
    """

    async def store_reflection(
        self,
        tenant_id: str,
        project_id: str,
        reflection_text: str,
        strategy_text: Optional[str],
        importance: float,
        confidence: float,
        tags: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """Store a new reflection and return its ID."""
        ...

    async def get_reflection(
        self,
        reflection_id: UUID,
        tenant_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a reflection by ID."""
        ...

    async def query_reflections(
        self,
        tenant_id: str,
        project_id: str,
        min_importance: float = 0.5,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Query reflections with filters."""
        ...


__all__ = [
    "MemoryRepositoryProtocol",
    "GraphRepositoryProtocol",
    "ReflectionRepositoryProtocol",
]
