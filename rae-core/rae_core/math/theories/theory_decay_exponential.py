"""
Theory: Exponential Temporal Decay (System 3.4 Revival)
Author: Gemini Agent (Archaeology Mode)
Refined: Robust handling of missing timestamps.
"""

import math
from datetime import datetime, timezone
from typing import Any, List, Dict
from uuid import UUID
from .base import IMathematicalTheory

class ExponentialDecayTheory(IMathematicalTheory):
    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        # Default half-life: 24 hours
        half_life = float(profile.get("math", {}).get("half_life_seconds", 86400))
        decay_rate = math.log(2) / half_life
        now = datetime.now(timezone.utc)
        
        results = []
        for c in candidates:
            # Calculate time difference with robust fallback
            created_at = c.get("created_at")
            
            # Convert string or existing datetime to UTC
            if isinstance(created_at, str):
                try: created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                except: created_at = now
            elif created_at is None:
                created_at = now
                
            # Ensure timezone awareness for subtraction
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            
            delta_t = (now - created_at).total_seconds()
            
            # Apply decay factor
            base_score = float(c.get("score", 0.5))
            decay_factor = math.exp(-decay_rate * max(0, delta_t))
            
            importance = float(c.get("metadata", {}).get("importance", 0.5))
            final_energy = base_score * (importance + 0.5) * decay_factor
            results.append((c["id"], final_energy))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results
