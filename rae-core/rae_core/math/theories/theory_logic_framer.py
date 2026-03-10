"""
Pillar 1: Logic Framer (Logos)
Strict deterministic matching for technical and industrial data.
Ensures that identifiers and codes have absolute priority.
"""

from typing import Any, List, Dict
from uuid import UUID
import re
from .base import IMathematicalTheory

class LogicFramerTheory(IMathematicalTheory):
    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        """
        Boosts results that contain exact symbols or technical codes from the query.
        """
        # 1. Extract symbols from query (Case-insensitive)
        # Using a simple but effective regex for technical IDs
        symbols = set(re.findall(r"[a-z0-9]{3,}(?:[-_][a-z0-9]+)+|0x[0-9a-f]+|ticket_\d+|err_\d+", query.lower()))
        
        if not symbols:
            # If no symbols in query, we don't apply logic framing boost
            return [(c["id"], float(c.get("score", 0.0))) for c in candidates]
            
        results = []
        # Multiplier for exact symbol matches - the "Scalpel" effect
        logic_boost_factor = float(profile.get("math", {}).get("logic_boost", 10.0))
        
        for c in candidates:
            content_lower = c.get("content", "").lower()
            score = float(c.get("score", 0.0))
            
            # Count how many query symbols are present in the candidate content
            match_count = sum(1 for s in symbols if s in content_lower)
            
            if match_count > 0:
                # Apply exponential boost based on match count
                # This ensures that a memory with 2 matching IDs is significantly better than 1.
                score = score * (logic_boost_factor ** match_count)
                
            results.append((c["id"], score))
            
        # Re-sort after boost to ensure determinism
        return sorted(results, key=lambda x: x[1], reverse=True)
