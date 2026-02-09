"""RAE Engine - The Intelligent Memory Manifold."""

from typing import Any

import numpy as np
import structlog

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
        math_controller: Any = None,
        resonance_engine: Any = None,
    ):
        self.memory_storage = memory_storage
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider
        self.llm_provider = llm_provider
        self.settings = settings

        # Initialize Math Layer Controller (The Brain)
        from rae_core.math.controller import MathLayerController
        from rae_core.math.resonance import SemanticResonanceEngine

        self.math_ctrl = math_controller or MathLayerController(config=settings)
        self.resonance_engine = resonance_engine or SemanticResonanceEngine(
            resonance_factor=0.4
        )

        # Modular Search Engine with ORB 4.0
        if search_engine:
            self.search_engine = search_engine
        else:
            from rae_core.search.engine import HybridSearchEngine

            self.search_engine = HybridSearchEngine(
                strategies={
                    "vector": self._init_vector_strategy(),
                    "fulltext": self._init_fulltext_strategy(),
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
        search_filters = {
            "agent_id": agent_id,
            "project": project,
            "layer": layer,
            **(filters or {}),
        }

        # Dynamic Weight Selection via Math Controller (Bandit)
        # If weights are provided in kwargs, they override the autonomous controller
        custom_weights = kwargs.get("custom_weights")

        # FIX: Distinguish between Retrieval Weights (dict) and Scoring Weights (object)
        strategy_weights = None
        if isinstance(custom_weights, dict):
            strategy_weights = custom_weights

        if not strategy_weights:
            # autonomous tuning
            strategy_weights = self.math_ctrl.get_retrieval_weights(query)
            logger.info("autonomous_tuning_applied", weights=strategy_weights)

        active_strategies = kwargs.get("strategies")

        candidates = await self.search_engine.search(
            query=query,
            tenant_id=tenant_id,
            filters=search_filters,
            limit=top_k * 5,  # Wide window for Math Layer
            strategies=active_strategies,
            strategy_weights=strategy_weights,
        )

        # 2. DESIGNED MATH SCORING (The Manifold)
        from rae_core.math.structure import ScoringWeights

        if isinstance(custom_weights, dict):
            # Extract only fields valid for ScoringWeights
            valid_fields = {
                k: v
                for k, v in custom_weights.items()
                if k in ["alpha", "beta", "gamma"]
            }
            scoring_weights = ScoringWeights(**valid_fields)
        elif custom_weights:
            scoring_weights = custom_weights
        else:
            scoring_weights = None  # Will use default in score_memory if None

        memories = []
        for m_id, sim_score in candidates:
            memory = await self.memory_storage.get_memory(m_id, tenant_id)
            if memory:
                # Math Layer weighs similarity against system-wide importance and topology
                math_score = self.math_ctrl.score_memory(
                    memory, query_similarity=sim_score, weights=scoring_weights
                )
                memory["math_score"] = math_score
                memory["search_score"] = sim_score
                memories.append(memory)

        # 3. SEMANTIC RESONANCE (Manifold Wave Propagation)
        # Using graph connectivity to boost non-obvious ideas
        if hasattr(self.memory_storage, "get_neighbors_batch") and memories:
            m_ids = [m["id"] for m in memories]
            edges = await self.memory_storage.get_neighbors_batch(m_ids, tenant_id)
            if edges:
                candidate_ids = {str(m["id"]) for m in memories}

                # Apply multi-hop resonance
                memories, energy_map = self.resonance_engine.compute_resonance(
                    memories, edges
                )

                # REFLECTION INDUCTION: Pull in new memories from the graph with high energy
                induced_ids = []
                # Threshold for induction (relative to top energy)
                if energy_map:
                    max_e = max(energy_map.values())
                    threshold = max_e * 0.4  # 40% of max energy

                    for node_id, energy in energy_map.items():
                        if node_id not in candidate_ids and energy > threshold:
                            induced_ids.append(node_id)

                # Fetch content for induced memories
                if induced_ids:
                    logger.info(
                        "reflection_induction_triggered", count=len(induced_ids)
                    )
                    for mid_str in induced_ids[
                        :5
                    ]:  # Limit induction to top 5 to avoid explosion
                        try:
                            from uuid import UUID

                            induced_mem = await self.memory_storage.get_memory(
                                UUID(mid_str), tenant_id
                            )
                            if induced_mem:
                                induced_mem["math_score"] = float(
                                    np.tanh(energy_map[mid_str])
                                )
                                induced_mem["resonance_metadata"] = {
                                    "induced": True,
                                    "boost": float(energy_map[mid_str]),
                                }
                                memories.append(induced_mem)
                        except Exception:
                            continue

        # 4. SYNERGY BOOST (Legacy compatibility for reflective layer)
        reflections = [m for m in memories if m.get("layer") == "reflective"]
        if reflections:
            for m in memories:
                if m.get("layer") != "reflective":
                    # Synergy boost from reflections (augmented by resonance)
                    m["math_score"] *= 1.2

        memories.sort(key=lambda x: x.get("math_score", 0.0), reverse=True)
        return memories[:top_k]

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text using the LLM provider.
        Used by ReflectionEngine and higher-level agentic patterns.
        """
        if not self.llm_provider:
            raise RuntimeError("LLM provider not configured in RAEEngine")

        from typing import cast

        return cast(
            str,
            await self.llm_provider.generate_text(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            ),
        )

    async def store_memory(self, **kwargs):
        """Store memory with automatic embedding."""
        content = kwargs.get("content")
        tenant_id = kwargs.get("tenant_id")
        m_id = await self.memory_storage.store_memory(**kwargs)

        # Automatic Vectorization (Manifold Entry)
        emb = await self.embedding_provider.embed_text(content)

        # Clean metadata for vector storage (remove heavy content)
        vector_meta = kwargs.copy()
        if "content" in vector_meta:
            del vector_meta["content"]

        await self.vector_store.store_vector(m_id, emb, tenant_id, metadata=vector_meta)
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
            },
        }

    async def run_reflection_cycle(self, **kwargs) -> dict[str, Any]:
        """Run memory consolidation/reflection cycle."""
        # Placeholder for reflection logic
        return {
            "status": "completed",
            "reflections_created": 0,
            "memories_consolidated": 0,
            "tokens_saved": 0,
        }
