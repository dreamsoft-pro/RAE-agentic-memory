import math
import os
import numpy as np
import structlog
from typing import List, Dict, Any, Tuple
from uuid import UUID
from rae_core.embedding.onnx_cross_encoder import OnnxCrossEncoder

logger = structlog.get_logger(__name__)

class LogicGateway:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.reranker = None
        
        # SYSTEM 22.2: Dynamic Path Resolution
        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        model_path = os.environ.get("RERANKER_MODEL_PATH") or os.path.join(project_root, "models/cross-encoder/model.onnx")
        tokenizer_path = os.environ.get("RERANKER_TOKENIZER_PATH") or os.path.join(project_root, "models/cross-encoder/tokenizer.json")
        
        if os.path.exists(model_path):
            try:
                self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
                logger.info("reranker_initialized", model=model_path)
            except Exception as e:
                logger.error("reranker_load_failed", error=str(e), path=model_path)
        else:
            logger.warning("reranker_model_missing", path=model_path)

    def route(self, query: str, strategy_results: Dict[str, List[Any]]) -> str:
        return "hybrid"

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def fuse(self, profile, strategy_results, weights=None, query="", config_override=None, memory_contents=None) -> List[Tuple[UUID, float]]:
        k = 60
        fused_scores: Dict[UUID, float] = {}
        candidate_data: Dict[UUID, Dict[str, Any]] = {}

        for strategy, results in strategy_results.items():
            weight = (weights or {}).get(strategy, 1.0)
            for rank, item in enumerate(results):
                # Handle different formats from adapters (Postgres vs SQLite)
                if isinstance(item, tuple):
                    m_id = item[0]
                elif isinstance(item, dict):
                    # Handle SQLite style nesting: {"memory": {...}, "score": ...}
                    if "memory" in item and "id" in item["memory"]:
                        m_id = item["memory"]["id"]
                    else:
                        m_id = item.get('id') or item.get('memory_id')
                    
                    if isinstance(m_id, str):
                        m_id = UUID(m_id)
                else:
                    continue
                
                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + weight * (1.0 / (rank + k))
                
                if m_id not in candidate_data:
                    content = (memory_contents or {}).get(m_id, "")
                    candidate_data[m_id] = {'id': m_id, 'content': content}

        candidates = []
        for m_id, score in fused_scores.items():
            data = candidate_data[m_id]
            data['rrf_score'] = score
            candidates.append(data)
        
        to_rerank = sorted(candidates, key=lambda x: x['rrf_score'], reverse=True)[:50]

        # Check if we have contents
        content_count = sum(1 for c in to_rerank if c['content'])
        
        if self.reranker and query and content_count > 0:
            pairs = []
            for c in to_rerank:
                text = c['content'] or "[no content]"
                pairs.append((query, text))
            
            logits = self.reranker.predict(pairs)
            
            for i, logit in enumerate(logits):
                prob = self.sigmoid(logit)
                to_rerank[i]['final_score'] = (prob * 10000) + to_rerank[i]['rrf_score']
            
            for c in candidates:
                if 'final_score' not in c:
                    c['final_score'] = c['rrf_score']
            
            logger.info("reranking_applied", best_prob=float(self.sigmoid(logits[0])) if len(logits)>0 else 0)
        else:
            for c in candidates:
                c['final_score'] = c['rrf_score']

        final_results = sorted(candidates, key=lambda x: x['final_score'], reverse=True)
        return [(c['id'], c['final_score']) for c in final_results]

    def process_query(self, query: str) -> str:
        return query.replace('"', '').strip()
