import math
import os
import re
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
        self, query: str, content: str, metadata: dict[str, Any] | None, h_sys: float
    ) -> tuple[float, dict[str, Any]]:
        """SYSTEM 72.1: Metadata-Driven Resolution (Fixed)."""
        q_lower = query.lower()
        content_lower = content.lower()
        evidence_bits = 0.0
        components = {"tier": 2}

        # 1. Symbolic Shield
        features = self.extractor.extract(query)
        if features.symbols:
            matched = sum(1 for s in features.symbols if s.lower() in content_lower)
            if matched > 0:
                match_ratio = matched / len(features.symbols)
                gain = match_ratio * h_sys
                evidence_bits += gain
                components["symbol_bits"] = round(gain, 2)
                if match_ratio == 1.0: 
                    components["hard_lock"] = True
                    components["tier"] = 0
                else:
                    components["tier"] = 1

        # 2. Metadata Sniper
        if metadata:
            sniper_fields = ["project", "agent_id", "author", "source", "layer"]
            field_matches = 0
            for field in sniper_fields:
                val = metadata.get(field)
                if val and str(val).lower() in q_lower:
                    evidence_bits += h_sys * 0.8
                    field_matches += 1
            
            if field_matches > 0:
                components["metadata_sniper_hits"] = field_matches
                if components["tier"] > 1: components["tier"] = 1

            importance = float(metadata.get("importance", 0.5))
            evidence_bits += importance
            components["importance_gain"] = round(importance, 2)

        return evidence_bits, components

    async def fuse(
        self,
        strategy_results,
        weights=None,
        query="",
        config_override=None,
        memory_contents=None,
        profile=None,
    ) -> list[tuple[UUID, float, float, dict]]:
        """SYSTEM 72.1: The Metadata Sniper Architecture."""
        import numpy as np
        
        max_seen = 0
        for res in strategy_results.values():
            if res: max_seen = max(max_seen, len(res))
        
        inferred_n = (config_override or {}).get("total_corpus_size")
        if not inferred_n:
            inferred_n = 1000.0
            if max_seen > 40: inferred_n = 10000.0
            if max_seen > 150: inferred_n = 100000.0
        
        h_sys = math.log2(float(inferred_n))
        ln2 = math.log(2)
        rerank_limit = int(h_sys * 35)
        
        logits_map: dict[UUID, float] = {}
        strategy_counts: dict[UUID, int] = {}
        
        # Heuristic Pre-sort
        for strategy, results in strategy_results.items():
            if not results: continue
            scores = [float(r[1]) for r in results if isinstance(r, tuple)]
            snr = (scores[0] - np.mean(scores)) / (np.std(scores) + 1e-6) if len(scores) > 1 else 1.0
            w_exp = math.log(snr + 2.0) * (weights or {}).get(strategy, 1.0)
            
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str): m_id = UUID(m_id)
                rank_logit = math.log(1.0 / (rank + 1.0))
                logits_map[m_id] = logits_map.get(m_id, 0.0) + (rank_logit * w_exp)
                strategy_counts[m_id] = strategy_counts.get(m_id, 0) + 1

        candidates = []
        for m_id, combined_logit in logits_map.items():
            synergy = strategy_counts[m_id]
            synergy_gain = math.log(synergy + 1.0) * h_sys
            candidates.append({"id": m_id, "logit": combined_logit + synergy_gain, "synergy": synergy})

        top_candidates = sorted(candidates, key=lambda x: x["logit"], reverse=True)[:rerank_limit]
        
        if self.reranker and query:
            pairs = []
            for c in top_candidates:
                mem_obj = (memory_contents or {}).get(c["id"], {})
                content = mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
                pairs.append((query, content))
            
            neural_scores = self.reranker.predict(pairs)
            for i, c in enumerate(top_candidates):
                c["neural_v"] = neural_scores[i]
                c["logit"] += neural_scores[i] * 2.0 

        processed = []
        for c in top_candidates:
            m_id = c["id"]
            mem_obj = (memory_contents or {}).get(m_id, {})
            content = mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
            meta = mem_obj.get("metadata", {}) if isinstance(mem_obj, dict) else {}
            if isinstance(meta, str):
                import json
                try: meta = json.loads(meta)
                except: meta = {}
            
            evidence_bits, components = self._apply_mathematical_logic(query, content, meta, h_sys)
            
            components["h_sys"] = round(h_sys, 2)
            components["synergy"] = c["synergy"]
            components["neural_v"] = round(c.get("neural_v", 0.0), 2)
            
            processed.append({
                "id": m_id,
                "tier": components["tier"],
                "evidence": evidence_bits,
                "neural": c.get("neural_v", 0.0),
                "synergy": c["synergy"],
                "logit": c["logit"] + (evidence_bits * ln2),
                "importance": float(meta.get("importance", 0.5)),
                "comp": components
            })

        # ABSOLUTE SORT: Tier -> Evidence -> Neural -> Synergy
        # Fixed sorting lambda (no negative on str)
        processed.sort(key=lambda x: (x["tier"], -x["evidence"], -x["neural"], -x["synergy"]))

        if processed:
            tau = 1.0 / (math.sqrt(h_sys) + 1.0)
            max_l = max(p["logit"] / tau for p in processed)
            exp_sum = sum(math.exp((p["logit"] / tau) - max_l) for p in processed)
            
            results = []
            for i, p in enumerate(processed):
                prob = math.exp((p["logit"] / tau) - max_l) / exp_sum
                if p["tier"] == 0 and i == 0: prob = max(prob, 0.9999)
                results.append((p["id"], prob, p["importance"], p["comp"]))
            
            return results
        
        return []

    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()
