import math
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple
from uuid import UUID
import structlog

from rae_core.embedding.onnx_cross_encoder import OnnxCrossEncoder
from rae_core.math.features_v2 import FeatureExtractorV2
from rae_core.math.metadata_injector import MetadataInjector
from rae_core.math.policy import PolicyRouter
from rae_core.math.fusion import Legacy416Strategy, SiliconOracleStrategy
from rae_core.math.resonance import SemanticResonanceEngine

logger = structlog.get_logger(__name__)

class LogicGateway:
    """
    RAE Logic Gateway (System 40.9)
    Hyper-Resolution Oracle with self-regulating Resonance.
    """
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.reranker = None
        self.extractor = FeatureExtractorV2()
        self.injector = MetadataInjector(self.config.get("injector"))
        self.router = PolicyRouter(
            confidence_threshold=self.config.get("confidence_threshold", 1.0)
        )
        
        # Strategy Registry
        self.strategies = {
            "legacy_416": Legacy416Strategy(),
            "silicon_oracle": SiliconOracleStrategy()
        }
        self.active_strategy_name = self.config.get("active_strategy", "legacy_416")

        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.path.join(project_root, "models/cross-encoder/model.onnx")
        tokenizer_path = os.path.join(project_root, "models/cross-encoder/tokenizer.json")

        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("reranker_initialized", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e))

    async def fuse(
        self,
        strategy_results: Dict[str, List[Any]],
        weights: Dict[str, float] | None = None,
        query: str = "",
        config_override: Dict[str, Any] | None = None,
        memory_contents: Dict[UUID, Dict[str, Any]] | None = None,
        profile: str | None = None,
    ) -> List[Tuple[UUID, float, float, Dict]]:
        """Dispatcher with Hyper-Resolution Resonance."""
        # 1. System Entropy
        max_seen = max([len(r) for r in strategy_results.values() if r] + [0])
        n_total = float((config_override or {}).get("total_corpus_size", 100000.0 if max_seen > 100 else 10000.0))
        h_sys = math.log2(n_total)
        
        # 2. Strategy Selection
        strategy_name = (config_override or {}).get("active_strategy") or self.active_strategy_name
        strategy = self.strategies.get(strategy_name, self.strategies["legacy_416"])
        
        # 3. Mathematical Base Fusion
        base_results = await strategy.fuse(
            strategy_results=strategy_results,
            query=query,
            h_sys=h_sys,
            memory_contents=memory_contents or {},
            weights=weights
        )
        
        # 4. SYSTEM 40.9: Signal Sharpening (Hyper-Resolution)
        # Convert base results to list of dicts for tuner
        tuner_input = []
        safe_contents = memory_contents or {}
        for m_id, score, importance, audit in base_results:
            tuner_input.append({
                "id": m_id, 
                "score": score, 
                "importance": importance, 
                "audit": audit,
                "content": safe_contents.get(m_id, {}).get("content", "")
            })
            
        tuner = SemanticResonanceEngine(h_sys=h_sys)
        sharpened_results = tuner.sharpen(query, tuner_input)
        
        # Convert back to standard tuple format for reranker
        results = [(r["id"], r["score"], r["importance"], r["audit"]) for r in sharpened_results]
        
        # 5. Mandatory Neural Scalpel (Post-processing for non-Tier 0/1)
        if self.reranker and query and results:
            window_size = max(30, int(h_sys * 10))
            # SYSTEM 42.0: ABSOLUTE ARMOR
            # We only rerank Tier 2. Tier 0 (Proof) and Tier 1 (Strong Match) are protected.
            to_rerank_indices = [i for i, r in enumerate(results[:window_size]) if r[3].get("tier", 2) >= 2]
            
            if to_rerank_indices:
                pairs = [(query, safe_contents.get(results[i][0], {}).get("content", "")) for i in to_rerank_indices]
                n_scores = self.reranker.predict(pairs)
                
                res_list = [list(r) for r in results]
                for idx, ri in enumerate(to_rerank_indices):
                    n_score = float(n_scores[idx])
                    # Neural score dominates within Tier 2
                    res_list[ri][1] = (n_score * 1000.0) + (res_list[ri][1] * 0.001)
                    res_list[ri][3]["neural_v"] = round(n_score, 2)
                    res_list[ri][3]["rerank_applied"] = True
                
                # Re-sort: Tier first (protected), then Score
                results = [tuple(r) for r in sorted(res_list, key=lambda x: (x[3].get("tier", 2), -x[1]))]

        return results


    def process_query(self, query: str) -> str:
        return query.replace('"', "").strip()
