"""
Modulator: Keyword Exclusivity (Tesla 3-6-9 Edition)
Penalizes 'noise words' that are present in the candidate but not in the query.
Used to ensure that technical, concise results win over long, rambling prose.
Essential for industrial logs where precision > recall.
"""

from typing import Any, List, Dict
from uuid import UUID
import re
from .base import IMathematicalTheory

class KeywordExclusivityTheory(IMathematicalTheory):
    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        # 1. Extract clean tokens from query (ignoring common junk)
        query_words = set(re.findall(r'\b[a-z0-9]{3,}\b', query.lower()))
        if not query_words:
            return [(c["id"], float(c.get("score", 0.0))) for c in candidates]
            
        results = []
        exclusivity_factor = float(profile.get("math", {}).get("exclusivity_weight", 0.8))
        
        for c in candidates:
            content = c.get("content", "").lower()
            score = float(c.get("score", 0.0))
            
            content_words = set(re.findall(r'\b[a-z0-9]{3,}\b', content))
            if not content_words:
                results.append((c["id"], score))
                continue
                
            # Count words in content that are NOT in query
            noise_words = content_words - query_words
            
            # Noise ratio: what % of document words are 'irrelevant'
            noise_ratio = len(noise_words) / len(content_words)
            
            # Apply penalty: score * (1.0 - (ratio * weight))
            # If 100% of words are noise, score drops significantly but not to 0
            penalty = 1.0 - (noise_ratio * exclusivity_factor)
            
            results.append((c["id"], score * max(0.1, penalty)))
            
        return sorted(results, key=lambda x: x[1], reverse=True)
