"""
RAE Semantic Resonance Engine (System 46.1).
Autonomous signal sharpening with Entropy-Driven Tiering.
"""

import math
import structlog
from typing import List, Dict, Any, Tuple
from uuid import UUID

logger = structlog.get_logger(__name__)

class SemanticResonanceEngine:
    """
    RAE Resonance Engine: Calculates Signal-to-Noise Ratio (SNR) for memories.
    Uses h_sys (corpus entropy) to scale strictness automatically.
    """
    
    def __init__(self, h_sys: float = 13.0, **kwargs):
        self.h_sys = h_sys # log2(corpus_size)

    def sharpen(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sharpens search signals by applying autonomous tiering based on SNR.
        """
        if not results or not query: return results

        q_lower = query.lower()
        q_tokens = set(q_lower.split())
        
        # Identify Technical Anchors (System 4.16 legacy + 46.1 logic)
        # Anchors are tokens likely to be IDs, codes, or specific terminology.
        anchors = [t for t in q_tokens if len(t) >= 8 or any(c.isdigit() for c in t) or any(c in t for c in "-_.:")]
        
        # Weight tokens: Anchors are far more important in industrial contexts
        # The boost factor scales with h_sys (higher corpus = stricter anchors)
        anchor_boost = 10.0 + self.h_sys
        token_weights = {t: len(t) * (anchor_boost if t in anchors else 1.0) for t in q_tokens}
        total_q_weight = sum(token_weights.values())

        sharpened_results = []
        
        # Autonomous Tiering Thresholds (Derived, not hardcoded)
        # Higher h_sys means we need higher coverage to reach Tier 0
        t0_threshold = max(0.5, min(0.95, 0.4 + (self.h_sys / 40.0)))
        t1_threshold = max(0.7, min(0.99, 0.6 + (self.h_sys / 40.0)))

        for res in results:
            content = res.get("content", "").lower()
            base_score = float(res.get("score") or 0.0)
            audit = res.get("audit") or {}
            
            # Calculate Semantic Coverage
            found_weight = sum(w for t, w in token_weights.items() if t in content)
            coverage = found_weight / total_q_weight if total_q_weight > 0 else 0
            
            # Tier Detection
            is_anchor_hit = len(anchors) > 0 and all(t in content for t in anchors)
            
            # TIER 0: Absolute Proof (Anchors matched + high coverage)
            if is_anchor_hit and coverage >= t0_threshold:
                audit["tier"] = 0
                final_score = 1e15 * coverage
            # TIER 1: Strong Consensus (Near perfect coverage)
            elif coverage >= t1_threshold:
                audit["tier"] = 1
                final_score = 1e12 * coverage
            # TIER 2: Probabilistic Signal (Needs Neural Scalpel)
            else:
                audit["tier"] = 2
                final_score = base_score
            
            audit.update({
                "res_v": 46.1,
                "h_sys": round(self.h_sys, 2),
                "coverage": round(coverage, 3),
                "thresholds": {"t0": round(t0_threshold, 2), "t1": round(t1_threshold, 2)}
            })
            
            res["score"] = final_score
            res["audit"] = audit
            sharpened_results.append(res)

        # Sort by Tier (Stability) then by Score (Precision)
        return sorted(
            sharpened_results, 
            key=lambda x: (x["audit"].get("tier", 2), -x["score"])
        )
