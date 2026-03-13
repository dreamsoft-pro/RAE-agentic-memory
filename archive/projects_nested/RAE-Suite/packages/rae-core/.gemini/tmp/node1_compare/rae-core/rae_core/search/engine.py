import logging
import math
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from rae_core.search.strategies import SearchStrategy

logger = logging.getLogger(__name__)


class FusionStrategy(ABC):
    @abstractmethod
    def fuse(
        self, results: dict[str, list[tuple[UUID, float]]], weights: dict[str, float]
    ) -> list[tuple[UUID, float]]:
        pass


class RRFFusion(FusionStrategy):
    def __init__(self, k: int = 60):
        self.k = k

    def fuse(
        self, results: dict[str, list[tuple[UUID, float]]], weights: dict[str, float]
    ) -> list[tuple[UUID, float]]:
        fused_scores: dict[UUID, float] = {}
        for strategy_name, strategy_results in results.items():
            weight = weights.get(strategy_name, 1.0)
            for rank, (m_id, _) in enumerate(strategy_results, 1):
                score = weight * (1.0 / (self.k + rank))
                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + score

        return sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)


class HybridSearchEngine:
    def __init__(
        self,
        strategies: dict[str, SearchStrategy],
        fusion_strategy: Any | None = None,
        cache: Any | None = None,
        math_controller: Any | None = None,
        embedding_provider: Any | None = None,
        memory_storage: Any | None = None,
    ):
        self.strategies = strategies
        self.fusion_strategy = fusion_strategy or RRFFusion()
        self.cache = cache
        self.math_controller = math_controller
        self.embedding_provider = embedding_provider
        self.memory_storage = memory_storage

    async def search(
        self,
        query: str,
        tenant_id: str,
        limit: int = 10,
        filters: dict[str, Any] | None = None,
        use_cache: bool = True,
        **kwargs: Any,
    ) -> list[tuple[UUID, float]]:
        active_strategy_names = kwargs.get("strategies") or list(self.strategies.keys())

        weights = {}
        if self.math_controller:
            weights = self.math_controller.get_weights(query, active_strategy_names)
        else:
            for name in active_strategy_names:
                strategy = self.strategies.get(name)
                weights[name] = (
                    strategy.get_strategy_weight()
                    if hasattr(strategy, "get_strategy_weight")
                    else 1.0
                )

        strategy_results: dict[str, list[tuple[UUID, float]]] = {}

        for name in active_strategy_names:
            strategy = self.strategies.get(name)
            if not strategy:
                continue
            try:
                p_id = (filters or {}).get("project")
                results = await strategy.search(
                    query=query,
                    tenant_id=tenant_id,
                    filters=filters,
                    limit=limit * 5,
                    project=p_id,
                )

                if results and len(results) > 1:
                    scores = [float(r[1]) for r in results]
                    min_s, max_s = min(scores), max(scores)
                    diff = max_s - min_s
                    if diff > 0.000001:
                        results = [
                            (r[0], (float(r[1]) - min_s) / diff) for r in results
                        ]
                    else:
                        results = [(r[0], 1.0) for r in results]
                strategy_results[name] = results or []
            except Exception as e:
                logger.error("strategy_failed", strategy=name, error=str(e))
                strategy_results[name] = []

        fused_results = self.fusion_strategy.fuse(strategy_results, weights)

        # ACTIVATE RERANKER if we have more than 1 result
        if len(fused_results) > 1 and self.embedding_provider and self.memory_storage:
            logger.info("reranking_activated", count=len(fused_results[:20]))
            return await self.rerank(query, fused_results[:20], tenant_id)

        return fused_results[:limit]

    async def rerank(
        self, query: str, results: list[tuple[UUID, float]], tenant_id: str
    ) -> list[tuple[UUID, float]]:
        """Emerald Reranker v1 - Semantic Cross-Validation."""
        try:
            query_emb = await self.embedding_provider.embed_text(query)
            reranked: list[tuple[UUID, float]] = []

            for m_id, original_score in results:
                # Get full content for deep comparison
                memory = await self.memory_storage.get_memory(m_id, tenant_id)
                if not memory:
                    reranked.append((m_id, original_score))
                    continue

                # Get or generate vector for the content
                mem_emb = await self.embedding_provider.embed_text(memory["content"])

                # Manual Cosine Similarity
                dot = sum(a * b for a, b in zip(query_emb, mem_emb))
                mag1 = math.sqrt(sum(a * a for a in query_emb))
                mag2 = math.sqrt(sum(b * b for b in mem_emb))
                semantic_score = dot / (mag1 * mag2) if (mag1 * mag2) > 0 else 0.0

                # Synergy Score: 70% Semantic, 30% Original Rank
                final_score = (semantic_score * 0.7) + (original_score * 0.3)
                reranked.append((m_id, final_score))

            return sorted(reranked, key=lambda x: x[1], reverse=True)
        except Exception as e:
            logger.error(f"rerank_failed: {str(e)}")
            return results
