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

        # Load resonance factor from config
        res_factor = self.math_ctrl.get_engine_param("resonance_factor", 0.4)

        self.resonance_engine = resonance_engine or SemanticResonanceEngine(
            resonance_factor=float(res_factor)
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
                },
                embedding_provider=self.embedding_provider,
                memory_storage=self.memory_storage,
            )

    def _init_vector_strategy(self):
        from rae_core.embedding.manager import EmbeddingManager

        if isinstance(self.embedding_provider, EmbeddingManager):
            from rae_core.search.strategies.multi_vector import (
                MultiVectorSearchStrategy,
            )

            strategies = []
            for name, provider in self.embedding_provider.providers.items():
                strategies.append((self.vector_store, provider, name))
            return MultiVectorSearchStrategy(strategies=strategies)

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
        search_filters = {**(filters or {})}
        if agent_id:
            search_filters["agent_id"] = agent_id
        if project:
            search_filters["project"] = project
        if layer:
            search_filters["layer"] = layer

        # 1. BANDIT TUNING: Get "weights" but interpret them as Threshold Signals (System 7.2)
        custom_weights = kwargs.get("custom_weights")
        strategy_weights = None

        if isinstance(custom_weights, dict):
            strategy_weights = custom_weights

        if not strategy_weights:
            strategy_weights = self.math_ctrl.get_retrieval_weights(query)
            logger.info("autonomous_tuning_applied", weights=strategy_weights)

        # --- SYSTEM 7.2: MAP WEIGHTS TO THRESHOLDS ---
        gateway_config_override = {}

        txt_w = strategy_weights.get("fulltext", 1.0)
        vec_w = strategy_weights.get("vector", 1.0)

        if txt_w >= 10.0:
            # Bandit signals "High Specificity" (Industrial/Log mode)
            gateway_config_override = {
                "confidence_gate": 0.95,  # Very strict early exit
                "rrf_k": 100,  # Flat ranking (Lexical dominates)
            }
        elif vec_w >= 5.0:
            # Bandit signals "High Abstraction"
            gateway_config_override = {
                "confidence_gate": 0.60,  # Loose early exit
                "rrf_k": 20,  # Aggressive ranking (Vector dominates)
            }

        # Prepare arguments safely
        active_strategies = kwargs.get("strategies")
        engine_limit = self.math_ctrl.get_engine_param("limit", 100)
        enable_reranking = kwargs.get("enable_reranking", False)

        # Clean kwargs to avoid duplicates in **search_kwargs
        search_kwargs = kwargs.copy()
        for k in [
            "strategies",
            "strategy_weights",
            "enable_reranking",
            "custom_weights",
        ]:
            search_kwargs.pop(k, None)

        if gateway_config_override:
            search_kwargs["gateway_config"] = gateway_config_override

        candidates = await self.search_engine.search(
            query=query,
            tenant_id=tenant_id,
            filters=search_filters,
            limit=int(engine_limit),
            strategies=active_strategies,
            strategy_weights=strategy_weights,
            enable_reranking=enable_reranking,
            math_controller=self.math_ctrl,
            **search_kwargs,
        )

        # 2. DESIGNED MATH SCORING
        from rae_core.math.structure import ScoringWeights

        scoring_weights = None
        if isinstance(custom_weights, dict):
            valid_fields = {
                k: v
                for k, v in custom_weights.items()
                if k in ["alpha", "beta", "gamma"]
            }
            scoring_weights = ScoringWeights(**valid_fields)
        elif custom_weights:
            scoring_weights = custom_weights

        memories = []
        for m_id, sim_score, importance in candidates:
            memory = await self.memory_storage.get_memory(m_id, tenant_id)
            if memory:
                math_score = self.math_ctrl.score_memory(
                    memory, query_similarity=sim_score, weights=scoring_weights
                )
                memory["math_score"] = math_score
                memory["search_score"] = sim_score
                memory["importance"] = importance  # Propagate importance from search
                memories.append(memory)

        # 3. SEMANTIC RESONANCE
        if hasattr(self.memory_storage, "get_neighbors_batch") and memories:
            m_ids = [m["id"] for m in memories]
            edges = await self.memory_storage.get_neighbors_batch(m_ids, tenant_id)
            if edges:
                candidate_ids = {str(m["id"]) for m in memories}
                memories, energy_map = self.resonance_engine.compute_resonance(
                    memories, edges
                )

                induced_ids = []
                if energy_map:
                    max_e = max(energy_map.values())
                    dyn_threshold = self.math_ctrl.get_resonance_threshold(query)
                    threshold = max_e * dyn_threshold

                    for node_id, energy in energy_map.items():
                        if node_id not in candidate_ids and energy > threshold:
                            induced_ids.append(node_id)

                if induced_ids:
                    logger.info(
                        "reflection_induction_triggered", count=len(induced_ids)
                    )
                    for mid_str in induced_ids[:5]:
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

        memories.sort(key=lambda x: x.get("math_score", 0.0), reverse=True)
        return memories[:top_k]

    async def generate_text(self, prompt: str, **kwargs) -> str:
        if not self.llm_provider:
            raise RuntimeError("LLM provider not configured")
        from typing import cast

        return cast(str, await self.llm_provider.generate_text(prompt=prompt, **kwargs))

    async def store_memory(self, **kwargs):
        content = kwargs.get("content")
        tenant_id = kwargs.get("tenant_id")
        m_id = await self.memory_storage.store_memory(**kwargs)

        if hasattr(self.embedding_provider, "generate_all_embeddings"):
            embs_dict = await self.embedding_provider.generate_all_embeddings(
                [content], task_type="search_document"
            )
            emb = {name: e[0] for name, e in embs_dict.items() if e}
        else:
            emb = await self.embedding_provider.embed_text(
                content, task_type="search_document"
            )

        vector_meta = kwargs.copy()
        if "content" in vector_meta:
            del vector_meta["content"]

        await self.vector_store.store_vector(m_id, emb, tenant_id, metadata=vector_meta)
        return m_id

    def get_status(self) -> dict[str, Any]:
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
        return {"status": "completed", "reflections_created": 0}
