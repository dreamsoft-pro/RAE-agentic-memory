import math
import os
from typing import Any, Dict, List, Tuple, Optional
from uuid import UUID
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
        
        # 3. Execution
        base_results = await strategy.fuse(
            strategy_results=strategy_results,
            query=query,
            h_sys=h_sys,
            memory_contents=memory_contents or {},
            weights=weights
        )
        
        # 4. Semantic Resonance (Hyper-Resolution)
        # Prepare input for resonance engine
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
        
        # Convert back to standard return format
        results = [(r["id"], r["score"], r["importance"], r["audit"]) for r in sharpened_results]
        
        # 5. Neural Scalpel (Reranking Tier 2+)
        if self.reranker and query and results:
            # We only rerank results that aren't mathematically proven (Tier 2)
            to_rerank_indices = [i for i, r in enumerate(results[:50]) if r[3].get("tier", 2) >= 2]
            
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
                        res_list[ri][1] = (n_val * 1000.0) + (res_list[ri][1] * 0.001)
                        res_list[ri][3]["neural_v"] = round(n_val, 3)
                    
                    # Re-sort within Tier 2, keeping Tier 0/1 on top
                    results = [tuple(r) for r in sorted(res_list, key=lambda x: (x[3].get("tier", 2), -x[1]))]

        return results
