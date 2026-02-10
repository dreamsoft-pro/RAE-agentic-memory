import math
import os
import json
from typing import Any
from uuid import UUID

import numpy as np
import structlog

from rae_core.embedding.onnx_cross_encoder import OnnxCrossEncoder
from rae_core.math.features_v2 import FeatureExtractorV2
from rae_core.math.metadata_injector import MetadataInjector
from rae_core.math.policy import PolicyRouter
from rae_core.math.resonance import SemanticResonanceEngine

logger = structlog.get_logger(__name__)


class LogicGateway:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.reranker = None
        self.extractor = FeatureExtractorV2()
        self.injector = MetadataInjector(self.config.get("injector"))
        self.graph_store = None
        self.storage = None
        self.router = PolicyRouter(confidence_threshold=0.4)

        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.path.join(project_root, "models/cross-encoder/model.onnx")
        tokenizer_path = os.path.join(project_root, "models/cross-encoder/tokenizer.json")

        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("reranker_initialized", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e))

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        if len(x) == 0: return x
        e_x = np.exp(x - np.max(x))
        return e_x / (e_x.sum() + 1e-9)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    async def fuse(
        self,
        strategy_results,
        weights=None,
        query="",
        config_override=None,
        memory_contents=None,
        profile=None,
    ) -> list[tuple[UUID, float]]:
        # SYSTEM 37.0: Hyper-Resolution Oracle
        candidate_data: dict[UUID, dict[str, Any]] = {}
        strategy_scores: dict[str, dict[UUID, float]] = {s: {} for s in strategy_results}

        for strategy, results in strategy_results.items():
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str): m_id = UUID(m_id)
                
                # Sharp exponential decay for rank
                strategy_scores[strategy][m_id] = math.exp(-rank / 3.0)

                if m_id not in candidate_data:
                    mem_obj = (memory_contents or {}).get(m_id, {})
                    metadata = mem_obj.get("metadata", {})
                    if isinstance(metadata, str):
                        try: metadata = json.loads(metadata)
                        except: metadata = {}
                    
                    candidate_data[m_id] = {
                        "id": m_id,
                        "content": mem_obj.get("content", "") if isinstance(mem_obj, dict) else "",
                        "metadata": metadata if isinstance(metadata, dict) else {},
                    }

        # Initial Fusion with Symbol Boost
        fused_scores: dict[UUID, float] = {}
        features = self.extractor.extract(query)
        
        for m_id in candidate_data:
            base_score = sum(strategy_scores[s].get(m_id, 0.0) for s in strategy_scores)
            
            # Symbolic Anchor (Multiplicative)
            if features.symbols:
                if any(sym.lower() in candidate_data[m_id]["content"].lower() for sym in features.symbols):
                    base_score *= 100.0
            
            fused_scores[m_id] = base_score

        # Global Resonance (5 iterations)
        if fused_scores and self.graph_store:
            try:
                res_engine = SemanticResonanceEngine(resonance_factor=0.5, iterations=5)
                initial_list = [ {**candidate_data[m_id], "search_score": fused_scores[m_id]} for m_id in fused_scores ]
                initial_list.sort(key=lambda x: x["search_score"], reverse=True)
                
                seed_ids = [str(c["id"]) for c in initial_list[:100]]
                edges = await self.graph_store.get_subgraph_edges(seed_ids)
                resonated, _ = res_engine.compute_resonance(initial_list[:100], edges)
                for r in resonated:
                    fused_scores[r["id"]] = r["math_score"]
            except Exception as e:
                logger.error("resonance_failed", error=str(e))

        candidates = [ {**candidate_data[m_id], "score": fused_scores[m_id]} for m_id in fused_scores ]
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        # Neural Tie-Breaker with Sigmoid Normalization
        to_rerank = candidates[:15]
        if self.reranker and query and to_rerank:
            pairs = []
            for c in to_rerank:
                m = c["metadata"]
                # Structure without noise
                ctx = f"[ID:{c['id']}] [P:{m.get('importance', 0.5)}]"
                pairs.append((query, f"{ctx} [CONTENT] {c['content']}"))

            logits = self.reranker.predict(pairs)
            for i, logit in enumerate(logits):
                # Sigmoid ensures logit is (0, 1), then we boost the top pick
                to_rerank[i]["score"] += self.sigmoid(float(logit)) * 10.0
            
            to_rerank.sort(key=lambda x: x["score"], reverse=True)
            return [(c["id"], c["score"]) for c in to_rerank]

        return [(c["id"], c["score"]) for c in candidates]

    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()