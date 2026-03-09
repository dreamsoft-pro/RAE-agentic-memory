"""
Theory Registry and Fluid Dispatcher.
Orchestrates the flow of mathematical theories over search results.
Integrated with Autonomous Theory Router.
"""

import structlog
from typing import Any, List, Dict, Type
from uuid import UUID
from .base import IMathematicalTheory
from .theory_decay_exponential import ExponentialDecayTheory
from .theory_resonance_quantum import QuantumResonanceTheory
from .theory_semantic_stability import SemanticStabilityTheory
from .router import TheoryRouter

logger = structlog.get_logger(__name__)

class TheoryRegistry:
    """Registry of available mathematical theories."""
    
    _theories: Dict[str, Type[IMathematicalTheory]] = {
        "decay": ExponentialDecayTheory,
        "resonance": QuantumResonanceTheory,
        "stability": SemanticStabilityTheory
    }
    
    @classmethod
    def get_theory(cls, name: str) -> IMathematicalTheory:
        theory_class = cls._theories.get(name)
        if not theory_class:
            raise ValueError(f"Theory '{name}' not found in registry.")
        return theory_class()

class FluidDispatcher:
    """
    Fluidly dispatches queries through a cascade of theories.
    Orchestrates the super-position of mathematical models based on router decisions.
    """
    
    def __init__(self, profile: Dict[str, Any] | None = None):
        self.profile = profile or {}
        self.router = TheoryRouter()
        
    def execute_cascade(self, candidates: List[Dict[str, Any]], query: str) -> List[tuple[UUID, float]]:
        """
        Executes a sequence of theories as decided by the Theory Router.
        """
        if not candidates:
            return []
            
        # 1. Start with initial scores
        current_results = [(c["id"], float(c.get("score", 0.5))) for c in candidates]
        
        # 2. Autonomous Route Selection
        theory_sequence = self.router.decide_sequence(query, self.profile)
        logger.info("theory_cascade_start", sequence=theory_sequence)
        
        # 3. Apply Theories in sequence (Fluid Flow)
        for theory_name in theory_sequence:
            try:
                theory = TheoryRegistry.get_theory(theory_name)
                # Chaining results fluidly
                pass_candidates = []
                for c_id, score in current_results:
                    orig = next((c for c in candidates if c["id"] == c_id), {})
                    pass_candidates.append({**orig, "score": score})
                
                current_results = theory.process(pass_candidates, query, self.profile)
            except Exception as e:
                logger.error("theory_execution_failed", theory=theory_name, error=str(e))
                
        return current_results
