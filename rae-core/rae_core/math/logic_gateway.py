import math
import os
from typing import Any, Dict, List, Tuple, Optional
from uuid import UUID
from datetime import datetime
import json
import structlog

from rae_core.embedding.onnx_cross_encoder import OnnxCrossEncoder
from rae_core.math.metadata_injector import MetadataInjector
from rae_core.math.resonance import SemanticResonanceEngine

logger = structlog.get_logger(__name__)

class LogicGateway:
    """
    RAE Logic Gateway (System 46.1)
    Central brain for search fusion, resonance, and neural reranking.
    """
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        
        # State injected by HybridSearchEngine
        self.storage = None 
        self.graph_store = None
        self.reranker = None
        
        self.injector = MetadataInjector(self.config.get("injector_config"))
        self._strategies = None

        # Automatic Model Loading (System 2.0 standard)
        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.path.join(project_root, "models/cross-encoder/model.onnx")
        tokenizer_path = os.path.join(project_root, "models/cross-encoder/tokenizer.json")

        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("neural_scalpel_ready", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e))

    @property
    def strategies(self):
        if self._strategies is None:
            # Lazy import to avoid circular dependencies
            from rae_core.math.fusion import Legacy416Strategy, SiliconOracleStrategy
            self._strategies = {
                "legacy_416": Legacy416Strategy(self.config),
                "silicon_oracle": SiliconOracleStrategy(self.config)
            }
        return self._strategies

    async def fuse(
        self,
        strategy_results: Dict[str, List[Any]],
        weights: Dict[str, float] | None = None,
        query: str = "",
        config_override: Dict[str, Any] | None = None,
        memory_contents: Dict[UUID, Dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> List[Tuple[UUID, float, float, Dict]]:
        """
        Silicon Oracle retreival pipeline.
        Combines mathematical base fusion with semantic resonance.
        """
        # 1. Autonomous h_sys calculation
        max_seen = max([len(r) for r in strategy_results.values() if r] + [0])
        # Scale complexity factor based on results density
        n_est = (config_override or {}).get("total_corpus_size", 100000.0 if max_seen > 100 else 10000.0)
        h_sys = math.log2(float(n_est))
        
        # 2. Base Strategy Dispatch
        active_mode = (config_override or {}).get("fusion_mode") or self.config.get("fusion_mode", "legacy_416")
        strategy = self.strategies.get(active_mode, self.strategies["legacy_416"])
        
        # SYSTEM 369.2: Apply Pillar Philosophical Weights (from Evolver)
        if weights:
            # genome format: {"pillars": {"logos": {"weight": 0.7}, ...}}
            # profile format: {"pillars": {"logos": {"weight": 0.7}, ...}}
            p_config = (config_override or self.config).get("pillars", {})
            if p_config:
                w_logos = float(p_config.get("logos", {}).get("weight", 1.0))
                w_psyche = float(p_config.get("psyche", {}).get("weight", 1.0))
                w_noos = float(p_config.get("noos", {}).get("weight", 1.0))
                
                # Apply multipliers to strategy weights
                if "fulltext" in weights: weights["fulltext"] *= w_logos
                if "vector_dense" in weights: weights["vector_dense"] *= w_psyche
                if "vector_nomic" in weights: weights["vector_nomic"] *= w_noos
                # Legacy compatibility
                if "vector" in weights: weights["vector"] *= w_psyche

        # 3. Execution (System 369.3 - Fluid Signal Fusion)
        base_results = await strategy.fuse(
            strategy_results=strategy_results,
            query=query,
            h_sys=h_sys,
            memory_contents=memory_contents or {},
            weights=weights
        )

        import re
        query_tokens = set(re.findall(r"\b(?:0x[0-9A-F]+|[a-z0-9]{3,}(?:[-_][a-z0-9]+)+|ticket_\d+|log_\d+|srv-\d+|incident_\d+)\b", query, re.I))

        # Signal Weights from Config (for Evolution)
        cfg_math = (config_override or self.config).get("math", {})
        w_id = float(cfg_math.get("identity_signal_weight", 100.0))
        w_shape = float(cfg_math.get("shape_signal_weight", 10.0))
        w_temp = float(cfg_math.get("temporal_signal_weight", 0.0000001)) # Tiny weight for huge timestamps

        boosted_results = []
        for r in base_results:
            m_id, score, importance, audit = r
            mem_data = (memory_contents or {}).get(m_id, {})
            content = str(mem_data.get("content", "")).lower()
            
            # A. Calculate Technical Signals
            # 1. Identity Lock (Exact Token Matches)
            id_count = sum(1 for t in query_tokens if t.lower() in content)
            id_signal = id_count * w_id
            
            # 2. Structural Shape Fit
            has_brackets = 1.0 if "[" in content and "]" in content else 0.0
            has_hex = 1.0 if "0x" in content else 0.0
            shape_signal = ((has_brackets + has_hex) / 2.0) * w_shape
            
            # 3. Temporal Signal (Relative to current time to avoid overflow)
            try:
                ts_str = mem_data.get("metadata", {}).get("timestamp", "")
                temp_v = datetime.fromisoformat(ts_str.replace('Z', '+00:00')).timestamp() if ts_str else 0.0
            except:
                temp_v = 0.0
            temp_signal = temp_v * w_temp

            # B. Apply Fast Path Short-Circuit (Tiering)
            is_anchor = False
            anchor_val = str(mem_data.get("metadata", {}).get("anchor") or "").lower()
            if anchor_val and any(t.lower() == anchor_val for t in query_tokens):
                is_anchor = True
                score = score * 1000.0 # Absolute priority for anchors
            
            # C. Fluid Fusion of All Signals
            final_score = score + id_signal + shape_signal + temp_signal
            
            new_audit = {
                **audit,
                "signals": {
                    "id": round(id_signal, 2),
                    "shape": round(shape_signal, 2),
                    "temp": round(temp_signal, 2)
                },
                "tier": 0 if is_anchor else 1,
                "fast_path": is_anchor
            }
            boosted_results.append((m_id, final_score, importance, new_audit))

        # Re-sort after fluid fusion
        base_results = sorted(boosted_results, key=lambda x: (x[3].get("tier", 2), -x[1]))
        
        # DEBUG: Trace input signals
        with open("DEBUG_FUSION.jsonl", "a") as f:
            log_entry = {
                "query": query,
                "strategy_results_counts": {k: len(v) for k, v in strategy_results.items()},
                "base_results_count": len(base_results),
                "timestamp": datetime.now().isoformat()
            }
            f.write(json.dumps(log_entry) + "\n")
        
        # 4. Semantic Resonance (Hyper-Resolution)
        # Prepare input for resonance engine
        tuner_input = []
        safe_contents = memory_contents or {}
        
        # SYSTEM 369.1: Layer Gravity Multipliers
        LAYER_WEIGHTS = {
            "reflective": 2.0,
            "semantic": 1.5,
            "working": 1.2,
            "episodic": 1.0
        }

        for m_id, score, importance, audit in base_results:
            mem_data = safe_contents.get(m_id, {})
            metadata = mem_data.get("metadata", {})
            layer = mem_data.get("layer", "episodic")
            
            # A. Layer Gravity (Cross-layer prioritization)
            layer_mult = LAYER_WEIGHTS.get(layer, 1.0)
            score = score * layer_mult
            
            # B. Human Label Priority (Logos Pillar)
            label = metadata.get("human_label", "").lower()
            if label and query.lower() in label:
                score = score * 5.0 # Potent boost for naming matches
                audit["label_hit"] = True
                audit["sic_boost"] = True # Silicon Oracle Hard-Lock

            tuner_input.append({
                "id": m_id, 
                "score": score, 
                "importance": importance, 
                "audit": audit,
                "content": mem_data.get("content", ""),
                "metadata": metadata
            })
            
        tuner = SemanticResonanceEngine(h_sys=h_sys)
        sharpened_results = tuner.sharpen(query, tuner_input)
        
        # 4.5. 3-6-9 Harmony Theory Cascade (Epistemological Refinement)
        # Apply specialized mathematical theories based on query domain (Tesla Edition)
        from rae_core.math.theories.registry import FluidDispatcher
        
        dispatcher = FluidDispatcher(profile=config_override or self.config)
        # FluidDispatcher expects list of candidates and query
        # Returns List[tuple[UUID, float]] (id, refined_score)
        refined_scores = dispatcher.execute_cascade(sharpened_results, query)
        
        # Update scores in sharpened_results based on theory cascade
        refined_map = {m_id: score for m_id, score in refined_scores}
        for r in sharpened_results:
            if r["id"] in refined_map:
                # Weighted fusion between sharpened and theory-refined scores
                # We give 70% weight to the theory cascade as it's more context-aware.
                r["score"] = (r["score"] * 0.3) + (refined_map[r["id"]] * 0.7)
        
        # Re-sort after theory fusion to ensure Rank 1 is actually the highest score
        sharpened_results = sorted(sharpened_results, key=lambda x: x["score"], reverse=True)
        
        # Convert back to standard return format
        results = [(r["id"], r["score"], r["importance"], r["audit"]) for r in sharpened_results]
        
        # 5. Neural Scalpel (Reranking Tier 1+)
        if self.reranker and query and results:
            # SYSTEM 40.10: Deep Recall (top 300) to find hidden hits
            # We rerank everything except Tier 0 (Hard Lock) to ensure semantic precision
            to_rerank_indices = [i for i, r in enumerate(results[:300]) if r[3].get("tier", 2) >= 1]
            
            if to_rerank_indices:
                pairs = [(query, safe_contents.get(results[i][0], {}).get("content", "")) for i in to_rerank_indices]
                # Filter out pairs with empty content
                valid_pairs = [p for p in pairs if p[1].strip()]
                
                if valid_pairs:
                    n_scores = self.reranker.predict(valid_pairs)
                    res_list = [list(r) for r in results]
                    
                    # Apply neural scores only to valid matches
                    for idx, ri in enumerate(to_rerank_indices[:len(n_scores)]):
                        n_val = float(n_scores[idx])
                        # Neural score becomes the primary signal for Tier 2
                        # but we MUST scale it by mathematical certainty (e.g. type match)
                        orig_audit = res_list[ri][3]
                        cert_factor = float(orig_audit.get("certainty_factor", 1.0))
                        
                        # Apply neural score scaled by certainty
                        # This ensures wrong entity types stay at the bottom regardless of neural score
                        res_list[ri][1] = (n_val * cert_factor * 1000.0) + (res_list[ri][1] * 0.001)
                        res_list[ri][3]["neural_v"] = round(n_val, 3)
                    
                    # Re-sort within Tier 2, keeping Tier 0/1 on top
                    # SYSTEM 40.11: Pure Tier Isolation. 
                    # We sort by (tier, -score). Since Tier 0 < Tier 1 < Tier 2,
                    # this guaranteed correct hits stay at the top.
                    results = [tuple(r) for r in sorted(res_list, key=lambda x: (x[3].get("tier", 2), -x[1]))]

        return results
