"""RAE Engine - The Intelligent Memory Manifold."""

from typing import Any, Dict, List, Tuple, Optional
from uuid import UUID
import structlog
from rae_core.search.fusion import RRFFusion

logger = structlog.get_logger(__name__)

class RAEEngine:
    """
    RAE Engine: A self-tuning memory manifold that uses designed math 
    to navigate vector spaces more intelligently than standard RAG.
    """
    def __init__(
        self,
        memory_storage: Any,
        vector_store: Any,
        embedding_provider: Any,
        llm_provider: Any = None,
        settings: Any = None,
        cache_provider: Any = None,
        search_engine: Any = None,
    ):
        self.memory_storage = memory_storage
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider
        self.llm_provider = llm_provider
        self.settings = settings
        
        # Modular Search Engine with ORB 4.0
        if search_engine:
            self.search_engine = search_engine
        else:
            from rae_core.search.engine import HybridSearchEngine
            self.search_engine = HybridSearchEngine(
                strategies={
                    "vector": self._init_vector_strategy(),
                    "fulltext": self._init_fulltext_strategy()
                }
            )

    def _init_vector_strategy(self):
        from rae_core.search.strategies.vector import VectorSearchStrategy
        return VectorSearchStrategy(self.vector_store, self.embedding_provider)

    def _init_fulltext_strategy(self):
        from rae_core.search.strategies.fulltext import FullTextStrategy
        return FullTextStrategy(self.memory_storage)

    async def search_memories(
        self,
        query: str,
        tenant_id: str,
        agent_id: str | None = None,
        layer: str | None = None,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
        project: str | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        RAE Reflective Search: Retrieval -> Math Scoring -> Manifold Adjustment.
        """
        # 1. RETRIEVAL (Vector + Keyword)
        # The search_engine uses ORB to balance these signals
        search_filters = {"agent_id": agent_id, "project": project, "layer": layer, **(filters or {})}
        
        # Avoid in-place modification of kwargs
        strategy_weights = kwargs.get("custom_weights", {}).copy() if kwargs.get("custom_weights") else None
        
        candidates = await self.search_engine.search(
            query=query, 
            tenant_id=tenant_id, 
            filters=search_filters,
            limit=top_k * 5, # Wide window for Math Layer
            strategy_weights=strategy_weights,
        )

        # 2. DESIGNED MATH SCORING (The Manifold)
        from rae_core.math.controller import MathLayerController
        from rae_core.math.structure import ScoringWeights
        math_ctrl = MathLayerController()
        
        raw_weights = kwargs.get("custom_weights")
        if isinstance(raw_weights, dict):
            # Extract only fields valid for ScoringWeights
            valid_fields = {k: v for k, v in raw_weights.items() if k in ["alpha", "beta", "gamma"]}
            scoring_weights = ScoringWeights(**valid_fields)
        else:
            scoring_weights = raw_weights
        
        memories = []
        for m_id, sim_score in candidates:
            memory = await self.memory_storage.get_memory(m_id, tenant_id)
            if memory:
                # Math Layer weighs similarity against system-wide importance and topology
                math_score = math_ctrl.score_memory(
                    memory, 
                    query_similarity=sim_score,
                    weights=scoring_weights
                )
                memory["math_score"] = math_score
                memory["search_score"] = sim_score
                memories.append(memory)

        # 3. REFLECTIVE RE-RANKING
        # If any Layer 4 (Reflective) memories are found, they boost their children
        reflections = [m for m in memories if m.get("layer") == "reflective"]
        if reflections:
            for m in memories:
                if m.get("layer") != "reflective":
                    # Synergy boost from reflections
                    m["math_score"] *= 1.5 

        memories.sort(key=lambda x: x.get("math_score", 0.0), reverse=True)
        return memories[:top_k]

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using the LLM provider.
        Used by ReflectionEngine and higher-level agentic patterns.
        """
        if not self.llm_provider:
            raise RuntimeError("LLM provider not configured in RAEEngine")
        
        return await self.llm_provider.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

    async def store_memory(self, **kwargs):
        """Store memory with automatic embedding."""
        content = kwargs.get("content")
        tenant_id = kwargs.get("tenant_id")
        m_id = await self.memory_storage.store_memory(**kwargs)
        
        # Automatic Vectorization (Manifold Entry)
        emb = await self.embedding_provider.embed_text(content)
        await self.vector_store.store_vector(m_id, emb, tenant_id, metadata=kwargs)
        return m_id

    def get_status(self) -> dict[str, Any]:
        """Get engine status and statistics."""
        return {
            "engine": "RAE-Core v2.9.0",
            "search_strategies": list(self.search_engine.strategies.keys()),
            "components": {
                "storage": type(self.memory_storage).__name__,
                "vector_store": type(self.vector_store).__name__,
                "embedding": type(self.embedding_provider).__name__,
            }
        }

    async def run_reflection_cycle(self, **kwargs) -> dict[str, Any]:
        """Run memory consolidation/reflection cycle."""
        # Placeholder for reflection logic
        return {
            "status": "completed",
            "reflections_created": 0,
            "memories_consolidated": 0,
            "tokens_saved": 0
        }