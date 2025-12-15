"""Abstract graph store interface for RAE-core.

This module defines the graph store interface for knowledge graph operations.
Implementations can use Neo4j, PostgreSQL with pg_graph, or in-memory graphs.
"""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class IGraphStore(ABC):
    """Abstract interface for graph storage and traversal.

    Implementations must provide graph storage for entity relationships
    and support for graph traversal operations (GraphRAG).
    """

    @abstractmethod
    async def create_node(
        self,
        node_id: UUID,
        node_type: str,
        tenant_id: str,
        properties: dict[str, Any] | None = None,
    ) -> bool:
        """Create a graph node.

        Args:
            node_id: UUID of the node (typically memory_id)
            node_type: Type of node (entity, concept, memory, etc.)
            tenant_id: Tenant identifier
            properties: Optional node properties

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def create_edge(
        self,
        source_id: UUID,
        target_id: UUID,
        edge_type: str,
        tenant_id: str,
        weight: float = 1.0,
        properties: dict[str, Any] | None = None,
    ) -> bool:
        """Create a graph edge.

        Args:
            source_id: UUID of source node
            target_id: UUID of target node
            edge_type: Type of relationship (relates_to, follows, causes, etc.)
            tenant_id: Tenant identifier
            weight: Edge weight (strength of relationship)
            properties: Optional edge properties

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_neighbors(
        self,
        node_id: UUID,
        tenant_id: str,
        edge_type: str | None = None,
        direction: str = "both",  # "in", "out", "both"
        max_depth: int = 1,
    ) -> list[UUID]:
        """Get neighboring nodes.

        Args:
            node_id: UUID of the node
            tenant_id: Tenant identifier
            edge_type: Optional filter by edge type
            direction: Traversal direction
            max_depth: Maximum traversal depth

        Returns:
            List of neighboring node UUIDs
        """
        pass

    @abstractmethod
    async def shortest_path(
        self,
        source_id: UUID,
        target_id: UUID,
        tenant_id: str,
        max_depth: int = 5,
    ) -> list[UUID] | None:
        """Find shortest path between two nodes.

        Args:
            source_id: UUID of source node
            target_id: UUID of target node
            tenant_id: Tenant identifier
            max_depth: Maximum path length

        Returns:
            List of node UUIDs in the path, or None if no path exists
        """
        pass

    @abstractmethod
    async def get_subgraph(
        self,
        node_ids: list[UUID],
        tenant_id: str,
        include_edges: bool = True,
    ) -> dict[str, Any]:
        """Extract a subgraph containing specified nodes.

        Args:
            node_ids: List of node UUIDs to include
            tenant_id: Tenant identifier
            include_edges: Whether to include edges between nodes

        Returns:
            Dictionary with 'nodes' and 'edges' lists
        """
        pass

    @abstractmethod
    async def delete_node(
        self,
        node_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a node and its edges.

        Args:
            node_id: UUID of the node
            tenant_id: Tenant identifier

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def delete_edge(
        self,
        source_id: UUID,
        target_id: UUID,
        edge_type: str,
        tenant_id: str,
    ) -> bool:
        """Delete an edge.

        Args:
            source_id: UUID of source node
            target_id: UUID of target node
            edge_type: Type of relationship
            tenant_id: Tenant identifier

        Returns:
            True if successful, False otherwise
        """
        pass
