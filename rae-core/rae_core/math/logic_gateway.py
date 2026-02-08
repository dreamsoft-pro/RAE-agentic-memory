import math
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
        model_path = "/app/models/cross-encoder/model.onnx"
        tokenizer_path = "/app/models/cross-encoder/tokenizer.json"
        
        try:
            self.reranker = OnnxCrossEncoder(model_path, tokenizer_path)
        except Exception as e:
            print(f"[LogicGateway] Reranker load failed: {e}")

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
                m_id = item[0] if isinstance(item, tuple) else (UUID(item['id']) if isinstance(item['id'], str) else item['id'])
                
                fused_scores[m_id] = fused_scores.get(m_id, 0.0) + weight * (1.0 / (rank + k))
                
                if m_id not in candidate_data:
                    # FETCH CONTENT FROM memory_contents
                    content = (memory_contents or {}).get(m_id, "")
                    candidate_data[m_id] = {'id': m_id, 'content': content}

        candidates = []
        for m_id, score in fused_scores.items():
            data = candidate_data[m_id]
            data['rrf_score'] = score
            candidates.append(data)
        
        to_rerank = sorted(candidates, key=lambda x: x['rrf_score'], reverse=True)[:50]

        # DEBUG: Check if we have contents
        content_count = sum(1 for c in to_rerank if c['content'])
        logger.info("rerank_context_check", total=len(to_rerank), with_content=content_count, query=query)

        if self.reranker and query and content_count > 0:
            pairs = []
            for c in to_rerank:
                # Use a placeholder if content is missing but some content exists in the batch
                text = c['content'] or "[no content]"
                pairs.append((query, text))
            
            logits = self.reranker.predict(pairs)
            
            for i, logit in enumerate(logits):
                prob = self.sigmoid(logit)
                to_rerank[i]['final_score'] = (prob * 10000) + to_rerank[i]['rrf_score']
            
            for c in candidates:
                if 'final_score' not in c:
                    c['final_score'] = c['rrf_score']
            
            logger.info("reranking_applied", best_prob=self.sigmoid(logits[0]) if len(logits)>0 else 0)
        else:
            for c in candidates:
                c['final_score'] = c['rrf_score']

        final_results = sorted(candidates, key=lambda x: x['final_score'], reverse=True)
        return [(c['id'], c['final_score']) for c in final_results]

    def process_query(self, query: str) -> str:
        return query.replace('"', '').strip()
