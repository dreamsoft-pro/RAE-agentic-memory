import math
import os
from typing import Any
from uuid import UUID

import structlog

from rae_core.embedding.onnx_cross_encoder import OnnxCrossEncoder
from rae_core.math.features_v2 import FeatureExtractorV2
from rae_core.math.metadata_injector import MetadataInjector
from rae_core.math.policy import PolicyRouter

logger = structlog.get_logger(__name__)


class LogicGateway:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.reranker = None
        self.extractor = FeatureExtractorV2()
        self.injector = MetadataInjector(self.config.get("injector"))
        self.graph_store = None
        self.storage = None
        self.router = PolicyRouter(
            confidence_threshold=self.config.get("confidence_threshold", 1.0)
        )

        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.environ.get("RERANKER_MODEL_PATH") or os.path.join(
            project_root, "models/cross-encoder/model.onnx"
        )
        tokenizer_path = os.environ.get("RERANKER_TOKENIZER_PATH") or os.path.join(
            project_root, "models/cross-encoder/tokenizer.json"
        )

        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("reranker_initialized", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e), path=model_path)
        else:
            logger.warning("reranker_model_missing", path=model_path)

    def route(self, query: str, strategy_results: dict[str, list[Any]]) -> str:
        return "hybrid"

    def sigmoid(self, x: float) -> float:
        """Numerically stable sigmoid."""
        try:
            if x >= 0:
                z = math.exp(-x)
                return 1 / (1 + z)
            else:
                z = math.exp(x)
                return z / (1 + z)
        except OverflowError:
            return 1.0 if x > 0 else 0.0

    def _apply_mathematical_logic(
        self, query: str, content: str, metadata: dict[str, Any] | None = None
    ) -> tuple[float, dict[str, float]]:
        import math
        import re

        q_lower = query.lower()
        content_lower = content.lower()
        multiplier = 1.0
        components = {}

        features = self.extractor.extract(query)
        if features.symbols:
            matched_symbols = 0
            total_symbols = len(features.symbols)
            for symbol in features.symbols:
                if symbol.lower() in content_lower: matched_symbols += 1
            if matched_symbols > 0:
                match_ratio = matched_symbols / total_symbols
                exponent = 100.0 if match_ratio == 1.0 else 10.0
                sic_boost = math.exp(match_ratio * exponent) 
                multiplier *= sic_boost
                components["sic_boost"] = sic_boost
                components["sic_matched"] = matched_symbols
                if match_ratio == 1.0: components["hard_lock"] = True

        doc_category = str(metadata.get("category", "")).lower() if metadata else ""
        if doc_category and doc_category in q_lower:
            cat_boost = math.e 
            multiplier *= cat_boost
            components["cat_boost"] = cat_boost

        return multiplier, components

    async def fuse(
        self,
        strategy_results,
        weights=None,
        query="",
        config_override=None,
        memory_contents=None,
        profile=None,
    ) -> list[tuple[UUID, float, float, dict]]:
        """
        SYSTEM 63.0: Neural Gateway (Scale Dominator).
        Uses Hierarchical Gating to break the 10k/100k noise floor.
        Automatically expands the neural verification zone based on corpus size.
        """
        import numpy as np
        import json
        
        n_total = float((config_override or {}).get("total_corpus_size", 1000.0))
        system_bit_depth = math.log2(n_total)
        
        # Dynamic Rerank Gating: In large datasets, we must verify more candidates neurally.
        # Scale: 1k -> 100, 10k -> 250, 100k -> 500
        rerank_limit = int(max(50, system_bit_depth * 20))
        base_sharpening = max(system_bit_depth / 4.0, 1.0)

        logits_map: dict[UUID, float] = {}
        strategy_contributions: dict[UUID, list[float]] = {}
        
        # 1. Expert Calibration
        expert_weights = {}
        strategy_taus = []
        for strategy, results in strategy_results.items():
            if not results: continue
            scores = [float(r[1]) for r in results if isinstance(r, tuple)]
            s_max, s_mean = scores[0], sum(scores)/len(scores)
            s_std = np.std(scores) if len(scores) > 1 else 0.1
            clarity = (s_max - s_mean) / (s_std + 1e-6)
            surprisal = -math.log2(len(results) / n_total)
            expert_reliability = (surprisal * base_sharpening) + math.log(clarity + 2.0)
            expert_weights[strategy] = expert_reliability * (weights or {}).get(strategy, 1.0)
            strategy_taus.append(3.0 / max(clarity, 0.5))

        tau = sum(strategy_taus) / len(strategy_taus) if strategy_taus else 3.0

        # 2. Fast Evidence Gathering
        for strategy, results in strategy_results.items():
            w_expert = expert_weights.get(strategy, 0.0)
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str): m_id = UUID(m_id)
                p = math.exp(-rank / tau) * 0.99
                evidence_logit = math.log(p / (1.0 - p))
                if rank < 5: evidence_logit *= base_sharpening
                logits_map[m_id] = logits_map.get(m_id, 0.0) + (evidence_logit * w_expert)
                if m_id not in strategy_contributions: strategy_contributions[m_id] = []
                strategy_contributions[m_id].append(1.0 / (rank + 1.0))

        # 3. Candidate Filtering & Quantum Bonus
        candidates = []
        for m_id, combined_logit in logits_map.items():
            synergy_count = len(strategy_contributions[m_id])
            coherence_bonus = (synergy_count ** 2) * system_bit_depth * 0.5
            final_logit = combined_logit + coherence_bonus
            if synergy_count >= 2 and combined_logit > system_bit_depth:
                final_logit += system_bit_depth * 10.0 # Truth Anchoring
            candidates.append({"id": m_id, "final_logit": final_logit, "synergy": synergy_count})

        # 4. Neural Expert Gating (Phase 2)
        # Select Top candidates for full neural verification
        top_candidates = sorted(candidates, key=lambda x: x["final_logit"], reverse=True)[:rerank_limit]
        
        final_results = []
        if self.reranker and query:
            pairs = []
            for c in top_candidates:
                mem_obj = (memory_contents or {}).get(c["id"], {})
                content = mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
                pairs.append((query, content))
            
            # Batch Reranking for speed
            neural_logits = self.reranker.predict(pairs)
            for i, c in enumerate(top_candidates):
                c["final_logit"] += neural_logits[i] * base_sharpening
                c["neural_score"] = neural_logits[i]

        # 5. Symbolic Hard-Lock & Purity Sort (Phase 3)
        for c in top_candidates:
            m_id = c["id"]
            mem_obj = (memory_contents or {}).get(m_id, {})
            content = mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
            meta = mem_obj.get("metadata", {}) if isinstance(mem_obj, dict) else {}
            if isinstance(meta, str):
                try: meta = json.loads(meta)
                except: meta = {}
            
            multiplier, components = self._apply_mathematical_logic(query, content, meta)
            actual_logit = c["final_logit"]
            
            if components.get("hard_lock"):
                actual_logit += (system_bit_depth * 100.0) # Absolute Winner
            else:
                actual_logit += math.log(max(multiplier, 1e-9))
            
            components["neural_v"] = round(c.get("neural_score", 0.0), 2)
            components["gate_limit"] = rerank_limit
            final_results.append((m_id, self.sigmoid(actual_logit), float(meta.get("importance", 0.5)), components))

        final_results.sort(key=lambda x: x[1], reverse=True)
        return final_results

    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()
