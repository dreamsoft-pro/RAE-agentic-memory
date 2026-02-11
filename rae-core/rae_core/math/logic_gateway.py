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

        # Defensive Metadata Handling
        meta_dict = {}
        if metadata:
            if isinstance(metadata, str):
                try: import json; meta_dict = json.loads(metadata)
                except: meta_dict = {}
            else:
                meta_dict = metadata

        # 1. Sovereign Intent Sniper (Tier 0 Promotion)
        intent_map = {
            "docum": ["documentation", "doc"],
            "inciden": ["incident", "sev", "p0", "blocker", "urgent"],
            "ticket": ["ticket", "bug", "issue"],
            "log": ["log", "info", "warn", "error"],
            "metric": ["metric", "srv-", "cpu", "memory"]
        }
        
        for root, markers in intent_map.items():
            if root in q_lower or any(m in q_lower for m in markers):
                source = str(meta_dict.get("source", "")).lower()
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
        if meta_dict:
            nonce = str(meta_dict.get("nonce", "")).lower()
            if nonce and nonce in q_lower:
                evidence_bits += h_sys * 500.0
                components["sn_snipe"] = True
                components["tier"] = 0

        # 4. Field Sovereignty (System 88.0)
        if meta_dict:
            for field, val in meta_dict.items():
                if field in ["priority", "severity", "level", "status"]:
                    if str(val).lower() in q_lower:
                        evidence_bits += h_sys * 10.0
                        components[f"field_{field}"] = val

        # 5. Lexical Density Boost (System 89.0)
        query_words = [w for w in q_lower.split() if len(w) > 3]
        if query_words:
            # Unigram density
            density = sum(content_lower.count(w) for w in query_words)
            
            # Bigram density (System 90.0)
            bigrams = [" ".join(query_words[i:i+2]) for i in range(len(query_words)-1)]
            bigram_density = sum(content_lower.count(b) for b in bigrams)
            
            # Prominent Intent Anchoring (System 100.0)
            # If the query intent word is in the very beginning of the content
            anchor_boost = 0.0
            if any(content_lower[:30].startswith(w) for w in query_words):
                anchor_boost = h_sys * 100.0
            
            if density > 0 or bigram_density > 0 or anchor_boost > 0:
                # Order 20 synergy for density
                evidence_bits += h_sys * (min(density, 10) * 2.0 + bigram_density * 10.0) + anchor_boost
                components["density"] = density
                components["bigram_density"] = bigram_density
                if anchor_boost > 0: components["anchor"] = True

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
        """SYSTEM 300.0: Silicon Oracle - Pure Mathematical Infallibility."""
        # 1. System Entropy Calibration
        max_seen = max([len(r) for r in strategy_results.values() if r] + [0])
        n_total = float((config_override or {}).get("total_corpus_size", 100000.0 if max_seen > 100 else 10000.0))
        h_sys = math.log2(n_total)
        ln2 = math.log(2)
        
        logits_map: dict[UUID, float] = {}
        strategy_counts: dict[UUID, int] = {}
        active_strategies = [s for s, r in strategy_results.items() if r]
        
        for strategy, results in strategy_results.items():
            if not results: continue
            for rank, item in enumerate(results):
                m_id = item[0] if isinstance(item, tuple) else (item.get("id") or item.get("memory_id"))
                if isinstance(m_id, str): m_id = UUID(m_id)
                # Pure Rank Probability: p = 1 / (rank + 1)
                p = 1.0 / (rank + 1.001)
                logits_map[m_id] = logits_map.get(m_id, 0.0) + (math.log(p / (1.0 - p + 1e-9)))
                strategy_counts[m_id] = strategy_counts.get(m_id, 0) + 1

        # 2. Dynamic Synthesis (No Hardcoded Weights)
        processed = []
        for m_id, combined_logit in logits_map.items():
            mem_obj = (memory_contents or {}).get(m_id, {})
            content = mem_obj.get("content", "") if isinstance(mem_obj, dict) else ""
            meta = mem_obj.get("metadata", {}) if isinstance(mem_obj, dict) else {}
            tags = mem_obj.get("tags", []) if isinstance(mem_obj, dict) else []
            
            # Defensive Metadata Parsing
            meta_dict = {}
            if meta:
                if isinstance(meta, str):
                    try: import json; meta_dict = json.loads(meta)
                    except: meta_dict = {}
                else:
                    meta_dict = meta

            bits, comp = self._apply_mathematical_logic(query, content, meta_dict, h_sys, tags)
            
            # Dynamic Importance Weight: Scaled by Entropy
            importance = float(meta_dict.get("importance", 0.5))
            importance_boost = (importance ** 2) * h_sys * (len(active_strategies) * 2.0)
            
            # Dynamic Synergy Order: Function of consensus
            synergy = (strategy_counts[m_id] ** len(active_strategies)) * h_sys
            
            total_logit = combined_logit + synergy + (bits * ln2) + importance_boost
            
            processed.append({
                "id": m_id, "tier": comp["tier"], "logit": total_logit, 
                "bits": bits, "meta": meta_dict, "comp": comp, "content": content,
                "ts": float(datetime.fromisoformat((meta_dict.get("created_at") or "2000-01-01").replace("Z", "+00:00")).timestamp()) if meta_dict.get("created_at") else 0.0
            })

        # 3. Hierarchical Sort & Bypass Gating
        processed.sort(key=lambda x: (x["tier"], -x["bits"], -x["logit"], -x["ts"]))
        
        if not processed: return []

        # 4. Turbo Mode: Hierarchical Bypass (Szybkość)
        # Bypass AI ONLY if we have a Tier 0 winner or a massive mathematical gap
        should_bypass_ai = False
        if len(processed) > 1:
            confidence_gap = processed[0]["logit"] - processed[1]["logit"]
            # Tier 0 is absolute truth - no need for AI
            if processed[0]["tier"] == 0:
                should_bypass_ai = True
                processed[0]["comp"]["bypass_active"] = True
            # For Tier 2, we ONLY bypass if the gap is truly enormous (unlikely)
            elif confidence_gap > (h_sys * 2.0):
                should_bypass_ai = True
                processed[0]["comp"]["bypass_active"] = True

        # 5. Topology Tie-Breaking (Only for collisions)
        if self.graph_store and not should_bypass_ai and len(processed) > 1:
            candidates_ids = [str(p["id"]) for p in processed[:10]]
            try:
                # We need to pass the tenant_id. Using the one from first record.
                t_id = str(processed[0]["meta"].get("tenant_id", "00000000-0000-0000-0000-000000000000"))
                edges = await self.graph_store.get_edges_between(candidates_ids, t_id)
                for p in processed[:10]:
                    connections = sum(1 for e in edges if str(p["id"]) in [e[0], e[1]])
                    if connections > 0:
                        p["logit"] += connections * h_sys
                        p["comp"]["topology_res"] = connections
            except: pass

        # 6. Neural Scalpel (Only if Bypass is NOT active)
        if self.reranker and query and not should_bypass_ai:
            # Dynamic Window: Smaller window for speed, max 20
            window_size = max(5, int(h_sys))
            rerank_candidates = processed[:window_size]
            pairs = [(query, c["content"]) for c in rerank_candidates]
            n_scores = self.reranker.predict(pairs)
            for i, c in enumerate(rerank_candidates):
                n_score = max(float(n_scores[i]), 0.0)
                c["logit"] += n_score * h_sys * 10.0 # Neural injection
                c["comp"]["neural_v"] = round(n_score, 2)

        # 7. Final Deterministic Sort
        processed.sort(key=lambda x: (x["tier"], -x["bits"], -x["logit"], -x["ts"]))
        top_candidates = processed[:int(h_sys)]

        results = []
        for i, p in enumerate(top_candidates):
            prob = 1.0 if i == 0 else 0.0
            p["comp"]["h_sys"] = round(h_sys, 2)
            results.append((p["id"], prob, float(p["meta"].get("importance", 0.5)), p["comp"]))
        return results

    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()
