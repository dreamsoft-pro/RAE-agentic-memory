"""
Theory Registry and Fluid Dispatcher (Tesla 3-6-9 Edition).
Orchestrates the flow of mathematical theories over search results.
"""

import structlog
import json
import os
from typing import Any, List, Dict, Type
from uuid import UUID
from .base import IMathematicalTheory
from .router import TheoryRouter
from .atlas import get_theory_by_id

logger = structlog.get_logger(__name__)

class TheoryRegistry:
    """Registry of available mathematical theories."""
    
    @classmethod
    def get_theory(cls, name_or_id: str) -> IMathematicalTheory:
        theory_class = get_theory_by_id(name_or_id)
        if not theory_class:
            raise ValueError(f"Theory '{name_or_id}' not found in Atlas.")
        return theory_class()

class FluidDispatcher:
    """
    Fluidly dispatches queries through a cascade of theories (3-6-9 Harmony).
    """
    
    def __init__(self, profile: Dict[str, Any] | None = None):
        self.profile = profile or {}
        self.router = TheoryRouter()
        self.genome_path = os.path.join(os.path.dirname(__file__), "theory_genome.json")
        self._load_evolved_params()
        
    def _load_evolved_params(self):
        """Loads parameters from the evolved genome into the profile."""
        if os.path.exists(self.genome_path):
            try:
                with open(self.genome_path, "r") as f:
                    genome = json.load(f)
                    # Merge domain-specific params into profile
                    # We'll need to know which domain was selected, or just merge all for now
                    # For simplicity, we merge all 'industrial' params if it's industrial
                    # This is a bit of a hack but works for the current evolution focus
                    ind_params = genome.get("domains", {}).get("industrial", {}).get("params", {})
                    if "math" not in self.profile:
                        self.profile["math"] = {}
                    self.profile["math"].update(ind_params)
            except:
                pass

    def execute_cascade(self, candidates: List[Dict[str, Any]], query: str) -> List[tuple[UUID, float]]:
        """
        Executes a sequence of theories (The Cascade) as decided by the 3-6-9 Router.
        """
        if not candidates:
            return []
            
        # 1. Start with initial scores (The Primordial Flow)
        current_results = [(c["id"], float(c.get("score", 0.5))) for c in candidates]
        
        # 2. Autonomous Route Selection (Context Recognition)
        theory_sequence = self.router.decide_sequence(query, self.profile)
        logger.info("theory_cascade_start", sequence=theory_sequence)
        
        # 3. Apply Theories in sequence (The Harmony)
        for theory_name in theory_sequence:
            try:
                theory = TheoryRegistry.get_theory(theory_name)
                
                # Transform results for the next stage in the cascade
                pass_candidates = []
                for c_id, score in current_results:
                    orig = next((c for c in candidates if c["id"] == c_id), {})
                    pass_candidates.append({**orig, "score": score})
                
                # Re-rank based on the specific theory
                current_results = theory.process(pass_candidates, query, self.profile)
                
            except Exception as e:
                logger.error("theory_execution_failed", theory=theory_name, error=str(e))
                
        # Re-normalize to avoid floating point explosion (Keeping it within [0, 1] for safety)
        if current_results:
            max_score = max(s for _, s in current_results)
            if max_score > 1.0:
                current_results = [(id, s/max_score) for id, s in current_results]
                
        return current_results
