"""
Modulator 6: Identity (Tesla 3-6-9 Edition)
The Sharpest Scalpel. Performs strict token-level identity matching.
Used for industrial IDs, HEX addresses, and serial numbers.
Provides a 'Binary Lock' - if ID matches, it's Rank 1.
"""

from typing import Any, List, Dict
from uuid import UUID
import re
from .base import IMathematicalTheory

class IdentityTheory(IMathematicalTheory):
    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        """
        Looks for high-entropy technical tokens in query and performs exact matching.
        """
        # Extract technical tokens (uppercase, numbers, special separators)
        # e.g., 0xABC, ID-123, ERROR_404
        tokens = set(re.findall(r"\b(?:0x[0-9A-F]+|[A-Z0-9]{3,}(?:[-_][A-Z0-9]+)+|[A-Z]{2,}\d+)\b", query))
        
        if not tokens:
            return [(c["id"], float(c.get("score", 0.0))) for c in candidates]
            
        results = []
        identity_lock_value = 1000000.0 # Extreme boost for identity match
        
        for c in candidates:
            content = c.get("content", "")
            score = float(c.get("score", 0.0))
            
            # Case-sensitive check for identity tokens
            matches = sum(1 for t in tokens if t in content)
            
            if matches > 0:
                # Identity Lock: This result IS the thing we are looking for
                score = identity_lock_value * matches
                
            results.append((c["id"], score))
            
        return sorted(results, key=lambda x: x[1], reverse=True)
