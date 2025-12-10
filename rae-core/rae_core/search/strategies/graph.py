"""Graph-based traversal search strategy (GraphRAG)."""

from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

from rae_core.interfaces.graph import IGraphStore
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.search.strategies import SearchStrategy


class GraphTraversalStrategy(SearchStrategy):
    """Graph-based search using relationship traversal.

    Implements GraphRAG by traversing memory relationships to find
    contextually connected memories.
    """

    def __init__(
        self,
        graph_store: IGraphStore,
        memory_storage: IMemoryStorage,
        default_weight: float = 0.2,
        max_depth: int = 2,
    ):
        """Initialize graph traversal strategy.

        Args:
            graph_store: Graph store implementation
            memory_storage: Memory storage for content retrieval
            default_weight: Default weight in hybrid search (0.0-1.0)
            max_depth: Maximum traversal depth
        """
        self.graph_store = graph_store
        self.memory_storage = memory_storage
        self.default_weight = default_weight
        self.max_depth = max_depth

    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[Tuple[UUID, float]]:
        """Execute graph traversal search.

        Args:
            query: Search query (can contain seed memory IDs)
            tenant_id: Tenant identifier
            filters: Optional filters (seed_ids, edge_type, max_depth)
            limit: Maximum number of results

        Returns:
            List of (memory_id, relevance_score) tuples
        """
        # Extract seed memory IDs from filters
        seed_ids = filters.get("seed_ids", []) if filters else []
        edge_type = filters.get("edge_type") if filters else None
        max_depth = filters.get("max_depth", self.max_depth) if filters else self.max_depth

        if not seed_ids:
            # If no seeds provided, return empty results
            # (Graph search requires starting points)
            return []

        # Traverse graph from seed nodes
        visited: Set[UUID] = set()
        results: Dict[UUID, float] = {}

        for seed_id in seed_ids:
            if isinstance(seed_id, str):
                seed_id = UUID(seed_id)

            # Get neighbors at each depth level
            neighbors = await self.graph_store.get_neighbors(
                node_id=seed_id,
                tenant_id=tenant_id,
                edge_type=edge_type,
                direction="both",
                max_depth=max_depth,
            )

            # Score by inverse depth (closer = higher score)
            for neighbor_id in neighbors:
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    # Simple scoring: inverse of depth + random factor
                    score = 1.0 / (max_depth + 1)
                    results[neighbor_id] = score

        # Convert to sorted list
        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        return sorted_results

    def get_strategy_name(self) -> str:
        """Return strategy name."""
        return "graph"

    def get_strategy_weight(self) -> float:
        """Return default weight for hybrid fusion."""
        return self.default_weight
