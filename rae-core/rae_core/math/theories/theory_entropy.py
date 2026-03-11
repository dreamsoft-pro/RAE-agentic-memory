"""
Modulator: Entropy (Tesla 3-6-9 Edition)
Penalizes high-entropy (noisy/generic) content to sharpen precision.
Ensures that short, precise technical matches win over long, rambling prose.
"""

from typing import Any, List, Dict
from uuid import UUID
import math
from .base import IMathematicalTheory

class EntropyTheory(IMathematicalTheory):
    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        entropy_weight = float(profile.get("math", {}).get("entropy_penalty", 0.5))
        results = []
        
        for c in candidates:
            content = c.get("content", "")
            score = float(c.get("score", 0.0))
            
            if not content:
                results.append((c["id"], score))
                continue
                
            # Calculate simple character-level entropy as proxy for noise
            chars = {}
            for char in content:
                chars[char] = chars.get(char, 0) + 1
            
            ent = 0.0
            for count in chars.values():
                p = count / len(content)
                ent -= p * math.log2(p)
            
            # Penalize results with very high entropy (too much variety/noise)
            # or very low entropy (repetitive/meaningless)
            penalty = 1.0
            if ent > 4.5: # Too noisy
                penalty = 1.0 - (ent - 4.5) * entropy_weight
            elif ent < 2.0: # Too simple/repetitive
                penalty = 0.8
                
            results.append((c["id"], score * max(0.1, penalty)))
            
        return sorted(results, key=lambda x: x[1], reverse=True)
