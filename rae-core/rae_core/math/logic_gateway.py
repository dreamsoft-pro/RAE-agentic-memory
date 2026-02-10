import math
import os
import re
from datetime import datetime
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
        self.router = PolicyRouter(
            confidence_threshold=self.config.get("confidence_threshold", 1.0)
        )

        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.path.join(project_root, "models/cross-encoder/model.onnx")
        tokenizer_path = os.path.join(project_root, "models/cross-encoder/tokenizer.json")

        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("reranker_initialized", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e))

    def sigmoid(self, x: float) -> float:
        try:
            if x >= 0: return 1 / (1 + math.exp(-x))
            z = math.exp(x)
            return z / (1 + z)
        except: return 1.0 if x > 0 else 0.0

    def _apply_mathematical_logic(
        self, query: str, content: str, metadata: dict[str, Any] | None, h_sys: float
    ) -> tuple[float, dict[str, Any]]:
        """SYSTEM 74.0: Emerald Sharpness Logic."""
        q_lower = query.lower()
        content_lower = content.lower()
        evidence_bits = 0.0
        components = {"tier": 2}

        # 1. Symbolic Imperative (Tier 0)
        features = self.extractor.extract(query)
        if features.symbols:
            matched = sum(1 for s in features.symbols if s.lower() in content_lower)
            if matched > 0:
                match_ratio = matched / len(features.symbols)
                # Emerald Boost: Power-scaling for extreme contrast
                gain = (match_ratio ** 2) * h_sys * 5.0 
                evidence_bits += gain
                if match_ratio == 1.0: 
                    components["hard_lock"] = True
                    components["tier"] = 0
                else: components["tier"] = 1

        # 2. Metadata Context
        if metadata:
            for field in ["project", "agent_id", "author", "source"]:
                val = metadata.get(field)
                if val and str(val).lower() in q_lower:
                    evidence_bits += h_sys * 2.0
                    components["tier"] = min(components["tier"], 1)

            importance = float(metadata.get("importance", 0.5))
            evidence_bits += importance * 2.0

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
        """SYSTEM 74.0: The Emerald Oracle (Sub-second Sniping)."""
        import numpy as np
        
        # 1. Scale Discovery
        max_seen = max([len(r) for r in strategy_results.values() if r] + [0])
        n_total = float((config_override or {}).get("total_corpus_size", 10000.0 if max_seen > 50 else 1000.0))
        h_sys = math.log2(n_total)
        ln2 = math.log(2)
        
        # Turbo Gating: Smaller rerank limit, but smarter L1
        rerank_limit = int(h_sys * 15) 
        
        logits_map: dict[UUID, float] = {}
        strategy_counts: dict[UUID, int] = {}
        
        # 2. Expert L1 Fusion with Emerald Sharpening
        for strategy, results in strategy_results.items():
            if not results: continue
            
            # Entropy Sharpening: Boost the winners, kill the noise
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str): m_id = UUID(m_id)
                
                # Exponential Rank Decay (Sharper than Boltzmann)
                p = math.exp(-rank / 2.0) 
                evidence_logit = math.log(p / (1.0 - p + 1e-9))
                
                logits_map[m_id] = logits_map.get(m_id, 0.0) + (evidence_logit * (weights or {}).get(strategy, 1.0))
                strategy_counts[m_id] = strategy_counts.get(m_id, 0) + 1

        # 3. Fast-Track Truth Detection
        candidates = []
        for m_id, combined_logit in logits_map.items():
            mem_obj = (memory_contents or {}).get(m_id, {})
            content = mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
            meta = mem_obj.get("metadata", {}) if isinstance(mem_obj, dict) else {}
            if isinstance(meta, str):
                try: import json; meta = json.loads(meta)
                except: meta = {}
            
            evidence_bits, components = self._apply_mathematical_logic(query, content, meta, h_sys)
            
            # The Emerald Filter: Synergy is non-linear
            synergy_bonus = (strategy_counts[m_id] ** 2) * h_sys
            total_logit = combined_logit + synergy_bonus + (evidence_bits * ln2)
            
            candidates.append({
                "id": m_id, "tier": components["tier"], "logit": total_logit, 
                "bits": evidence_bits, "meta": meta, "comp": components,
                "ts": float(datetime.fromisoformat((meta.get("created_at") or "2000-01-01").replace("Z", "+00:00")).timestamp()) if meta.get("created_at") else 0.0
            })

        # 4. Hierarchical Resolution (No AI if Tier 0 is found)
        candidates.sort(key=lambda x: (x["tier"], -x["bits"], -x["logit"], -x["ts"]))
        top_candidates = candidates[:rerank_limit]
        
        # 5. Smart Neural Gating (Only for Tier 2 or close ties)
        if self.reranker and query and (len(top_candidates) > 1 and top_candidates[0]["tier"] > 0):
            pairs = [(query, (memory_contents or {}).get(c["id"], {}).get("content", "")) for c in top_candidates]
            n_scores = self.reranker.predict(pairs)
            for i, c in enumerate(top_candidates):
                c["logit"] += n_scores[i] * h_sys
                c["comp"]["neural_v"] = round(float(n_scores[i]), 2)

        # 6. Final Probability Calibration
        if top_candidates:
            tau = 1.0 / (h_sys + 1.0) # Cold softmax for high contrast
            max_l = max(c["logit"] for c in top_candidates)
            exp_sum = sum(math.exp((c["logit"] - max_l) / tau) for c in top_candidates)
            
            results = []
            for i, c in enumerate(top_candidates):
                prob = math.exp((c["logit"] - max_l) / tau) / exp_sum
                if i == 0 and c["tier"] == 0: prob = 1.0 # Absolute Truth
                c["comp"]["h_sys"] = round(h_sys, 2)
                results.append((c["id"], prob, float(c["meta"].get("importance", 0.5)), c["comp"]))
            
            return results
        return []

    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()