"""Hybrid search engine implementation."""

import math
from typing import Any, Dict, List, Tuple
from uuid import UUID

import structlog

from rae_core.interfaces.embedding import IEmbeddingProvider
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.interfaces.reranking import IReranker
from rae_core.math.fusion import FusionStrategy
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
        candidates: List[Tuple[UUID, float]],
        tenant_id: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> List[Tuple[UUID, float]]:
        if self.embedding_provider is None or self.memory_storage is None:
            return candidates[:limit]

        try:
            query_emb = await self.embedding_provider.embed_text(
                query, task_type="search_query"
            )
            reranked: List[Tuple[UUID, float]] = []

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


class HybridSearchEngine:
    """
    Orchestrates multiple search strategies (Vector + FullText) and fuses them using LogicGateway.
    """

    def __init__(
        self,
        strategies: Dict[str, SearchStrategy],
        embedding_provider: IEmbeddingProvider,
        memory_storage: IMemoryStorage,
        reranker: IReranker | None = None,
    ):
        self.strategies = strategies
        self.embedding_provider = embedding_provider
        self.memory_storage = memory_storage
        self._reranker = reranker
        
        # Initialize Fusion Strategy (LogicGateway wrapper)
        self.fusion_strategy = FusionStrategy()

    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: Dict[str, Any] | None = None,
        limit: int = 10,
        strategies: List[str] | None = None,
        strategy_weights: Dict[str, float] | None = None,
        enable_reranking: bool = False,
        math_controller: Any = None,
        **kwargs: Any,
    ) -> List[Tuple[UUID, float]]:
        """
        Execute search across active strategies and fuse results.
        Supports System 7.2 gateway_config override.
        """
        active_strategies = strategies or list(self.strategies.keys())
        weights = strategy_weights or {}
        
        # Extract Gateway Config Override (System 7.2)
        gateway_config = kwargs.get("gateway_config")

        # 1. PARALLEL EXECUTION
        # (Ideally asyncio.gather, but doing sequential for now)
        strategy_results: Dict[str, List[Tuple[UUID, float]]] = {}
        
        for name in active_strategies:
            if name not in self.strategies:
                continue
                
            strategy = self.strategies[name]
            try:
                # Pass down kwargs (like vector_name)
                results = await strategy.search(
                    query=query,
                    tenant_id=tenant_id,
                    filters=filters,
                    limit=limit,
                    **kwargs
                )
                strategy_results[name] = results
            except Exception as e:
                logger.error("strategy_failed", name=name, error=str(e))
                strategy_results[name] = []

        # 2. FUSION (LogicGateway)
        # Note: We pass 'gateway_config' to fuse if supported
        fused_results = self.fusion_strategy.fuse(
            strategy_results, 
            weights, 
            query=query, 
            config_override=gateway_config
        )
        
        # 3. OPTIONAL RERANKING
        if enable_reranking and len(fused_results) > 1:
            reranker = self._reranker
            if reranker is None and self.embedding_provider and self.memory_storage:
                reranker = EmeraldReranker(self.embedding_provider, self.memory_storage)

            if reranker:
                logger.info("reranking_activated", count=len(fused_results[:20]))
                return await reranker.rerank(
                    query, fused_results[:20], tenant_id, limit=limit
                )
            
        return fused_results[:limit]