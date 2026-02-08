from typing import Any
from uuid import UUID

from ...interfaces.graph import IGraphStore
from . import SearchStrategy


class GraphTraversalStrategy(SearchStrategy):
    """Search strategy using graph traversal from seed memories."""

    def __init__(self, graph_store: IGraphStore, default_weight: float = 0.5) -> None:
        self.graph_store = graph_store
        self.default_weight = default_weight

    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
        project: str | None = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float, float]]:
        # Graph search usually needs seed IDs
        seed_ids = kwargs.get("seed_ids", [])
        if not seed_ids:
            return []

        # Placeholder for real graph logic
        return []

    def get_strategy_name(self) -> str:
        return "graph"

    def get_strategy_weight(self) -> float:
        return self.default_weight
