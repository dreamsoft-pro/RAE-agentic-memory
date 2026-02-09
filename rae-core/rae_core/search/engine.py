"""Hybrid search engine implementation."""

import math
from typing import Any
from uuid import UUID

import structlog

from rae_core.interfaces.embedding import IEmbeddingProvider
from rae_core.interfaces.reranking import IReranker
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.math.fusion import FusionStrategy
from rae_core.math.metadata_injector import MetadataInjector
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
        candidates: list[tuple[UUID, float, float]],
        tenant_id: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[tuple[UUID, float, float]]:
        if self.embedding_provider is None or self.memory_storage is None:
            return candidates[:limit]

        try:
            query_emb = await self.embedding_provider.embed_text(
                query, task_type="search_query"
            )
            reranked: list[tuple[UUID, float, float]] = []

            for item in candidates:
                m_id, original_score, importance = self._unpack_candidate(item)
                
                # Get full content for deep comparison
                memory = await self.memory_storage.get_memory(m_id, tenant_id)
                if not memory:
                    reranked.append((m_id, original_score, importance))
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
                reranked.append((m_id, final_score, importance))

            return sorted(reranked, key=lambda x: x[1], reverse=True)[:limit]
        except Exception as e:
            logger.error("rerank_failed", error=str(e))
            return candidates[:limit]

    def _unpack_candidate(self, item: tuple) -> tuple[UUID, float, float]:
        """Safely unpack candidate tuple (handles 2 or 3 values)."""
        if len(item) == 3:
            return item[0], item[1], item[2]
        elif len(item) == 2:
            return item[0], item[1], 0.0
        else:
            raise ValueError(f"Invalid candidate tuple length: {len(item)}")


class HybridSearchEngine:
    """
    Orchestrates multiple search strategies (Vector + FullText) and fuses them using LogicGateway.
    """

    def __init__(
        self,
        strategies: dict[str, SearchStrategy],
        embedding_provider: IEmbeddingProvider,
        memory_storage: IMemoryStorage,
        reranker: IReranker | None = None,
    ):
        self.strategies = strategies
        self.embedding_provider = embedding_provider
        self.memory_storage = memory_storage
        self._reranker = reranker
        self.injector = MetadataInjector()

        # Initialize Fusion Strategy (LogicGateway wrapper)
        self.fusion_strategy = FusionStrategy()

    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
        strategies: list[str] | None = None,
        strategy_weights: dict[str, float] | None = None,
        enable_reranking: bool = False,
        math_controller: Any = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float, float]]:
        """
        Execute search across active strategies and fuse results.
        Supports System 7.2 gateway_config override.
        """
        active_strategies = strategies or list(self.strategies.keys())
        weights = strategy_weights or {}

        # Extract Gateway Config Override (System 7.2)
        gateway_config = kwargs.get("gateway_config")

        # Metadata Injection (System 23.0) - Always on for better candidate sets
        enriched_query = self.injector.process_query(query)
        if enriched_query != query:
            logger.info("query_enriched", original=query, enriched=enriched_query)

        # 1. PARALLEL EXECUTION
        strategy_results: dict[str, list[tuple[UUID, float, float]]] = {}

        for name in active_strategies:
            if name not in self.strategies:
                continue

            strategy = self.strategies[name]
            try:
                # Pass down kwargs (like vector_name)
                results = await strategy.search(
                    query=enriched_query,
                    tenant_id=tenant_id,
                    filters=filters,
                    limit=limit,
                    **kwargs,
                )
                # Ensure results are 3-value tuples for robustness
                strategy_results[name] = [
                    (r[0], r[1], r[2] if len(r) > 2 else 0.0) for r in results
                ]
            except Exception as e:
                logger.error("strategy_failed", name=name, error=str(e))
                strategy_results[name] = []

        # 2. FUSION (LogicGateway)
        # Fetch contents for reranking
        all_ids = set()
        for results in strategy_results.values():
            for r in results:
                all_ids.add(r[0]) # m_id

        memory_data = {}
        if all_ids and hasattr(self.memory_storage, "get_memories_batch"):
            try:
                mems = await self.memory_storage.get_memories_batch(
                    list(all_ids), tenant_id
                )
                for mem in mems:
                    # Store full memory object instead of just content
                    memory_data[mem["id"]] = mem
            except Exception as e:
                logger.warning("batch_fetch_failed", error=str(e))

        # Note: We pass 'gateway_config' to fuse if supported
        fused_results = self.fusion_strategy.fuse(
            strategy_results,
            weights,
            query=enriched_query,
            config_override=gateway_config,
            memory_contents=memory_data,
        )

        # 3. OPTIONAL RERANKING
        if enable_reranking and len(fused_results) > 1:
            # Skip if LogicGateway already reranked (Neural Scalpel active)
            if hasattr(self.fusion_strategy, "gateway") and self.fusion_strategy.gateway.reranker:
                return fused_results[:limit]

            reranker = self._reranker
            if reranker is None and self.embedding_provider and self.memory_storage:
                reranker = EmeraldReranker(self.embedding_provider, self.memory_storage)

            if reranker:
                logger.info("reranking_activated", count=len(fused_results[:20]))
                return await reranker.rerank(
                    enriched_query, fused_results[:20], tenant_id, limit=limit
                )

        return fused_results[:limit]
