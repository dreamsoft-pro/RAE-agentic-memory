"""
Theory Atlas (Atlas Teorii) - Tesla 3-6-9 Edition
Central registry for the RAE Epistemological Engine.
"""

from typing import Dict, List, Type, Any
from .base import IMathematicalTheory
from .theory_logic_framer import LogicFramerTheory
from .theory_resonance_quantum import QuantumResonanceTheory
from .theory_semantic_stability import SemanticStabilityTheory
from .theory_decay_exponential import ExponentialDecayTheory
from .theory_synergy import SynergyTheory
from .theory_entropy import EntropyTheory

# Poziom 3: Trzy Filary Bytu (Pillars)
PILLARS = {
    "logos": LogicFramerTheory,      # Pillar 1: Lexical/Deterministic (Concrete)
    "psyche": SemanticStabilityTheory, # Pillar 2: Semantic/Intuitive (Stability)
    "noos": QuantumResonanceTheory     # Pillar 3: Relational/Context (Resonance)
}

# Poziom 6: Sześciu Modulatorów (Modulators)
MODULATORS = {
    "decay": ExponentialDecayTheory,
    "resonance": QuantumResonanceTheory,
    "stability": SemanticStabilityTheory,
    "synergy": SynergyTheory,
    "entropy": EntropyTheory,
    # Future additions: Gravity
}

# Poziom 9: Dziewięć Domen Świata (Domain Profiles)
DOMAINS = {
    "industrial": ["logos", "synergy", "entropy", "decay"],
    "medical": ["psyche", "noos", "synergy"],
    "legal": ["logos", "psyche", "noos"],
    "it_support": ["logos", "synergy", "noos"],
    "creative": ["psyche", "noos"],
    "administrative": ["stability", "decay"],
    "scientific": ["noos", "stability", "synergy"],
    "personal": ["psyche", "decay"],
    "security": ["logos", "entropy", "stability"]
}

def get_theory_by_id(theory_id: str) -> Type[IMathematicalTheory] | None:
    """Helper to find theory in any level of the 3-6-9 hierarchy."""
    all_theories = {**PILLARS, **MODULATORS}
    return all_theories.get(theory_id)
