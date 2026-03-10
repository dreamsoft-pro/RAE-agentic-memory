"""
Additional Strategy: Structural Gravity (Tesla 3-6-9 Edition)
Analyzes the 'Shape' of the query and candidates.
Ensures that technical logs attract other technical logs, 
while prose attracts prose. Prevents 'Semantic Drift' between 
incident reports and raw log lines.
"""

from typing import Any, List, Dict
from uuid import UUID
import re
from .base import IMathematicalTheory

class StructuralGravityTheory(IMathematicalTheory):
    def _get_shape_score(self, text: str) -> float:
        """Determines if text is a TECHNICAL log (1.0) or PROSE (0.0)."""
        if not text: return 0.0
        
        # Log markers: timestamps, level brackets, HEX, low word count
        has_ts = 1.0 if re.search(r'\d{2}:\d{2}:\d{2}', text) else 0.0
        has_level = 1.0 if re.search(r'\[(ERROR|WARN|INFO|DEBUG|CRITICAL)\]', text, re.I) else 0.0
        has_hex = 1.0 if re.search(r'0x[0-9A-F]+', text, re.I) else 0.0
        
        word_count = len(text.split())
        is_short = 1.0 if word_count < 15 else 0.0
        
        # Average shape score
        return (has_ts + has_level + has_hex + is_short) / 4.0

    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        query_shape = self._get_shape_score(query)
        results = []
        
        # Gravity factor: how much we trust the shape match
        gravity_mult = float(profile.get("math", {}).get("gravity_factor", 5.0))
        
        for c in candidates:
            content = c.get("content", "")
            score = float(c.get("score", 0.0))
            candidate_shape = self._get_shape_score(content)
            
            # If query and candidate have the same shape, boost gravity
            # (1.0 - diff) * multiplier
            shape_match = 1.0 - abs(query_shape - candidate_shape)
            
            if shape_match > 0.7:
                score = score * (1.0 + (shape_match * gravity_mult))
                
            results.append((c["id"], score))
            
        return sorted(results, key=lambda x: x[1], reverse=True)
