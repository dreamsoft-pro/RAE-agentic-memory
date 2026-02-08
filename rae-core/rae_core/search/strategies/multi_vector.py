from typing import Any
from uuid import UUID

from ...interfaces.embedding import IEmbeddingProvider
from ...interfaces.vector import IVectorStore
from . import SearchStrategy


class MultiVectorSearchStrategy(SearchStrategy):
    """Hybrid search strategy using multiple vector spaces."""

    def __init__(
        self,
        strategies: list[tuple[IVectorStore, IEmbeddingProvider, str]],
        default_weight: float = 1.0,
    ) -> None:
        self.strategies_list = strategies
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
        # This strategy uses multiple vector stores/models
        # For simplicity, we implement a basic version that just takes the first one
        # or would ideally gather from all and fuse.

        if not self.strategies_list:
            return []

        store, embedder, name = self.strategies_list[0]

        query_embedding = await embedder.embed_text(query, task_type="search_query")
        results = await store.search_similar(
            query_embedding=query_embedding,
            tenant_id=tenant_id,
            limit=limit,
            vector_name=name,
            **kwargs,
        )

        return [(r[0], r[1], 0.0) for r in results]

    def get_strategy_name(self) -> str:
        return "multi_vector"

    def get_strategy_weight(self) -> float:
        return self.default_weight
