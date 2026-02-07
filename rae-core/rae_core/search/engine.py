import math
from abc import ABC, abstractmethod
from typing import Any, cast
from uuid import UUID

import structlog

from rae_core.interfaces.reranking import IReranker
from rae_core.search.strategies import SearchStrategy

logger = structlog.get_logger(__name__)


class EmeraldReranker(IReranker):
    """Emerald Reranker v1 - Semantic Cross-Validation."""

    def __init__(self, embedding_provider: Any, memory_storage: Any):
        self.embedding_provider = embedding_provider
        self.memory_storage = memory_storage

    async def rerank(
        self,
        query: str,
        candidates: list[tuple[UUID, float]],
        tenant_id: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[tuple[UUID, float]]:
        if self.embedding_provider is None or self.memory_storage is None:
            return candidates[:limit]

        try:
            query_emb = await self.embedding_provider.embed_text(
                query, task_type="search_query"
            )
            reranked: list[tuple[UUID, float]] = []

            for m_id, original_score in candidates:
                # Get full content for deep comparison
                memory = await self.memory_storage.get_memory(m_id, tenant_id)
                if not memory:
                    reranked.append((m_id, original_score))
                    continue

                # Get or generate vector for the content
                mem_emb = await self.embedding_provider.embed_text(
                    memory["content"], task_type="search_document"
                )

                # Manual Cosine Similarity
                dot = sum(a * b for a, b in zip(query_emb, mem_emb))
                mag1 = math.sqrt(sum(a * a for a in query_emb))
                mag2 = math.sqrt(sum(b * b for b in mem_emb))
                semantic_score = dot / (mag1 * mag2) if (mag1 * mag2) > 0 else 0.0

                # Synergy Score: 70% Semantic, 30% Original Rank
                final_score = (semantic_score * 0.7) + (original_score * 0.3)
                reranked.append((m_id, final_score))

            return sorted(reranked, key=lambda x: x[1], reverse=True)[:limit]
        except Exception as e:
            logger.error("rerank_failed", error=str(e))
            return candidates[:limit]


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
        reranker: IReranker | None = None,
    ):
        self.strategies = strategies
        
        # System 4.0: Logic-based stability
        from rae_core.math.fusion import LogicFusion
        self.fusion_strategy = fusion_strategy or LogicFusion()
        
        self.cache = cache
        self.math_controller = math_controller
        self.embedding_provider = embedding_provider
        self.memory_storage = memory_storage
        self._reranker = reranker

    async def search(
        self,
        query: str,
        tenant_id: str,
        limit: int = 10,
        filters: dict[str, Any] | None = None,
        use_cache: bool = True,
        enable_reranking: bool = True,
        **kwargs: Any,
    ) -> list[tuple[UUID, float]]:
        # 1. Check Cache
        if use_cache and self.cache:
            cached = await self.cache.get(query, tenant_id, filters=filters, **kwargs)
            if cached:
                logger.info("search_cache_hit", query=query)
                return cast(list[tuple[UUID, float]], cached[:limit])

        active_strategy_names = kwargs.get("strategies") or list(self.strategies.keys())

        # SYSTEM 6.0: PARALLEL DUAL-ENGINE (Math Unbound)
        # For datasets < 10GB (MES, Logistics), Global FullText is fast enough and provides superior recall for technical data.
        # We do NOT restrict FullText by Vector results (Cascade). We run them in parallel and FUSE them.

        strategy_results: dict[str, list[tuple[UUID, float]]] = {}
        
        # 1. Vector Search (Parallel)
        vector_strategy = self.strategies.get("vector")
        tensor_ids: list[UUID] = []
        if vector_strategy:
            try:
                # Fetch semantic candidates
                fetch_limit = 2000 
                tensor_results = await vector_strategy.search(
                    query=query,
                    tenant_id=tenant_id,
                    filters=filters,
                    limit=fetch_limit,
                    **kwargs,
                )
                tensor_ids = [id for id, _ in tensor_results]
                strategy_results["vector"] = tensor_results[:500] # Pass top 500 to fusion
            except Exception as e:
                logger.error("vector_search_failed", error=str(e))
                strategy_results["vector"] = []

        # 2. Lexical/Math Search (Parallel - Global Scope)
        weights = {}
        if self.math_controller:
            weights = self.math_controller.get_weights(query, active_strategy_names)

        scoped_filters = (filters or {}).copy()
        # CRITICAL CHANGE: We do NOT add 'memory_ids': tensor_ids to filters.
        # FullText searches the ENTIRE index. This ensures 100% Recall for technical tokens.

        for name in active_strategy_names:
            if name == "vector": continue # Already done
            
            strategy = self.strategies.get(name)
            if not strategy:
                continue

            try:
                p_id = (filters or {}).get("project")
                # Global Search Limit: 500 is safe for performance, but 1000 gives better Recall for noisy logs.
                # Since we are fusion-based, getting more candidates is better.
                global_limit = 1000 
                
                results = await strategy.search(
                    query=query,
                    tenant_id=tenant_id,
                    filters=scoped_filters, # Global filters (tenant/agent), NO vector constraint
                    limit=global_limit,
                    project=p_id,
                    **kwargs,
                )
                strategy_results[name] = results or []
            except Exception as e:
                logger.error("strategy_failed", strategy=name, error=str(e))
                strategy_results[name] = []

        # System 4.0: Fusion
        if hasattr(self.fusion_strategy, "fuse"):
            try:
                fused_results = self.fusion_strategy.fuse(strategy_results, weights, query=query)
            except TypeError:
                fused_results = self.fusion_strategy.fuse(strategy_results, weights)
        else:
            fused_results = []

        # Update Cache
        if use_cache and self.cache:
            await self.cache.set(
                query, tenant_id, fused_results, filters=filters, **kwargs
            )

        # ACTIVATE RERANKER
        if enable_reranking and len(fused_results) > 1:
            reranker = self._reranker
            if reranker is None and self.embedding_provider and self.memory_storage:
                reranker = EmeraldReranker(self.embedding_provider, self.memory_storage)

            if reranker:
                return await reranker.rerank(
                    query, fused_results[:20], tenant_id, limit=limit
                )

        return fused_results[:limit]
