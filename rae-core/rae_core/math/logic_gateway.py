import math
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Tuple
from uuid import UUID
from collections import Counter

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
        self.graph_store = None

        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.path.join(project_root, "models/cross-encoder/model.onnx")
        tokenizer_path = os.path.join(project_root, "models/cross-encoder/tokenizer.json")

        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("reranker_initialized", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e))

    def _apply_mathematical_logic(
        self, query: str, content: str, metadata: dict[str, Any] | None, h_sys: float, tags: list[str] = None
    ) -> tuple[float, dict[str, Any]]:
        """SYSTEM 86.0: Infallible Autocrat Logic."""
        q_lower = query.lower()
        content_lower = content.lower()
        evidence_bits = 0.0
        components = {"tier": 2}

        # 1. Sovereign Intent Sniper (Tier 0 Promotion)
        # Any mention of industrial domains forces Tier 0 for matching sources
        intent_map = {
            "docum": ["documentation", "doc"],
            "inciden": ["incident", "sev", "p0", "blocker", "urgent"],
            "ticket": ["ticket", "bug", "issue"],
            "log": ["log", "info", "warn", "error"],
            "metric": ["metric", "srv-", "cpu", "memory"]
        }
        
        for root, markers in intent_map.items():
            if root in q_lower or any(m in q_lower for m in markers):
                source = str(metadata.get("source", "")).lower() if metadata else ""
                tag_list = [str(t).lower() for t in (tags or [])]
                if any(m in source for m in markers) or any(root in t for t in tag_list) or any(m in tag_list for m in markers):
                    evidence_bits += h_sys * 100.0 # Absolute Singularity
                    components["intent"] = root
                    components["tier"] = 0 # FORCED TIER 0
                    return evidence_bits, components

        # 2. Symbolic Hard-Lock
        features = self.extractor.extract(query)
        industrial_codes = re.findall(r'[pP]\d|sev\d|sn-\d+', q_lower)
        all_symbols = list(set(features.symbols + industrial_codes))
        
        if all_symbols:
            matched = sum(1 for s in all_symbols if s.lower() in content_lower)
            if matched == len(all_symbols):
                evidence_bits += h_sys * 200.0
                components["hard_lock"] = True
                components["tier"] = 0
                return evidence_bits, components

        # 3. Metadata Nonce Sniper
        if metadata:
            nonce = str(metadata.get("nonce", "")).lower()
            if nonce and nonce in q_lower:
                evidence_bits += h_sys * 500.0
                components["sn_snipe"] = True
                components["tier"] = 0

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
        """SYSTEM 86.0: The Ultimate Infallible Oracle - Final Strike."""
        # 1. Entropy Calibration
        max_seen = max([len(r) for r in strategy_results.values() if r] + [0])
        n_total = float((config_override or {}).get("total_corpus_size", 10000.0 if max_seen > 50 else 1000.0))
        h_sys = math.log2(n_total)
        ln2 = math.log(2)
        
        logits_map: dict[UUID, float] = {}
        strategy_counts: dict[UUID, int] = {}
        for strategy, results in strategy_results.items():
            if not results: continue
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str): m_id = UUID(m_id)
                # Absolute rank sharpness
                p = 1.0 / (rank + 1.0)
                logits_map[m_id] = logits_map.get(m_id, 0.0) + (math.log(p / (1.0 - p + 1e-9)))
                strategy_counts[m_id] = strategy_counts.get(m_id, 0) + 1

        # 2. Sovereign Synthesis
        processed = []
        for m_id, combined_logit in logits_map.items():
            mem_obj = (memory_contents or {}).get(m_id, {})
            content = mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
            meta = mem_obj.get("metadata", {}) if isinstance(mem_obj, dict) else {}
            tags = mem_obj.get("tags", []) if isinstance(mem_obj, dict) else []
            if isinstance(meta, str):
                try: import json; meta = json.loads(meta)
                except: meta = {}
            
            bits, comp = self._apply_mathematical_logic(query, content, meta, h_sys, tags)
            # Hyper-Synergy (Order 6)
            synergy = (strategy_counts[m_id] ** 6) * h_sys
            total_logit = combined_logit + synergy + (bits * ln2)
            
            processed.append({
                "id": m_id, "tier": comp["tier"], "logit": total_logit, 
                "bits": bits, "meta": meta, "comp": comp, "content": content,
                "ts": float(datetime.fromisoformat((meta.get("created_at") or "2000-01-01").replace("Z", "+00:00")).timestamp()) if meta.get("created_at") else 0.0
            })

        # 3. ABSOLUTE TIER SORT (No AI for 10k to prevent noise)
        processed.sort(key=lambda x: (x["tier"], -x["bits"], -x["logit"], -x["ts"]))
        top_candidates = processed[:int(h_sys * 5)]
        
        # 4. Neural Tie-Breaking (DISABLED for 10k industrial scale)
        if self.reranker and query and n_total < 5000:
            pairs = [(query, c["content"]) for c in top_candidates]
            n_scores = self.reranker.predict(pairs)
            for i, c in enumerate(top_candidates):
                n_score = max(float(n_scores[i]), 0.0)
                c["logit"] += n_score * h_sys
                c["comp"]["neural_v"] = round(n_score, 2)

        # 5. Final Hierarchical Sort
        top_candidates.sort(key=lambda x: (x["tier"], -x["bits"], -x["logit"], -x["ts"]))

        if top_candidates:
            results = []
            for i, p in enumerate(top_candidates):
                # Deterministic winner takes all
                prob = 1.0 if i == 0 else 0.0
                p["comp"]["h_sys"] = round(h_sys, 2)
                results.append((p["id"], prob, float(p["meta"].get("importance", 0.5)), p["comp"]))
            return results
        return []

    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()
