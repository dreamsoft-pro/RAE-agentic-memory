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
        default_weight: float = 0.5,
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
        """Search across all registered vector spaces and fuse results."""
        if not self.strategies_list:
            return []

        # Gather results from all providers
        all_results: dict[str, list[tuple[UUID, float, float]]] = {}

        for store, embedder, name in self.strategies_list:
            try:
                query_embedding = await embedder.embed_text(
                    query, task_type="search_query"
                )
                results = await store.search_similar(
                    query_embedding=query_embedding,
                    tenant_id=tenant_id,
                    limit=limit,
                    vector_name=name,
                    **kwargs,
                )
                all_results[name] = [(r[0], r[1], 0.0) for r in results]
            except Exception:
                continue

        if not all_results:
            return []

        # Simple Exponential Rank Sharpening for multi-vector
        import math
        fused_scores: dict[UUID, float] = {}
        for strategy_res in all_results.values():
            for rank, (m_id, _, _) in enumerate(strategy_res):
                # Using the same constant as System 37.0 for consistency
                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + math.exp(-rank / 3.0)

        # Sort and return
        final = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [(m_id, score, 0.0) for m_id, score in final]

    def get_strategy_name(self) -> str:
        return "multi_vector_fusion"

    def get_strategy_weight(self) -> float:
        return self.default_weight
