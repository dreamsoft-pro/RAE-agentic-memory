"""
Theory: Kalman Semantic Stability (RAE Native)
Author: Gemini Agent (Control Theory Mode)
Principle: Uses a 1D Kalman Filter to smooth noisy importance and similarity scores.
           Filters out stochastic anomalies in search results by treating scores as
           measurements from a dynamic system.
"""

from typing import Any, List, Dict
from uuid import UUID
from .base import IMathematicalTheory
from rae_core.math.stability import SimpleKalmanFilter

class SemanticStabilityTheory(IMathematicalTheory):
    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        # Initialize Kalman Filter with parameters from profile
        # R: Measurement noise, Q: Process noise
        r = float(profile.get("math", {}).get("kalman_r", 0.1))
        q = float(profile.get("math", {}).get("kalman_q", 0.01))
        
        kf = SimpleKalmanFilter(r=r, q=q)
        results = []
        
        # Sort by initial score to establish a 'baseline' for the filter
        # In this theory, the filter 'tracks' the decay of similarity across the result set
        initial_list = sorted(candidates, key=lambda x: float(x.get("score", 0.0)), reverse=True)
        
        for c in initial_list:
            raw_score = float(c.get("score", 0.0))
            importance = float(c.get("metadata", {}).get("importance", 0.5))
            
            # Combine raw score with importance as the 'measurement'
            measurement = (raw_score + importance) / 2.0
            
            # Update filter and get smoothed state
            stable_score = kf.update(measurement)
            
            results.append((c["id"], stable_score))
            
        # Re-sort based on stabilized energy
        results.sort(key=lambda x: x[1], reverse=True)
        return results
