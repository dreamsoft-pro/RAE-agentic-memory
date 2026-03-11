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
from .theory_identity import IdentityTheory
from .theory_structural_gravity import StructuralGravityTheory
from .theory_exclusivity import KeywordExclusivityTheory

# Poziom 3: Trzy Filary Bytu (Pillars)
PILLARS = {
    "logos": IdentityTheory,         # Pillar 1: Pure Identity / Determinism
    "psyche": SemanticStabilityTheory, # Pillar 2: Semantic/Intuitive (Stability)
    "noos": QuantumResonanceTheory     # Pillar 3: Relational/Context (Resonance)
}

# Poziom 6: Sześciu Modulatorów (Modulators)
MODULATORS = {
    "identity": IdentityTheory,
    "logos": IdentityTheory,        # Alias for Evolver
    "logic": LogicFramerTheory,
    "decay": ExponentialDecayTheory,
    "resonance": QuantumResonanceTheory,
    "noos": QuantumResonanceTheory, # Alias
    "stability": SemanticStabilityTheory,
    "psyche": SemanticStabilityTheory, # Alias
    "synergy": SynergyTheory,
    "entropy": EntropyTheory,
    "gravity": StructuralGravityTheory,
    "exclusivity": KeywordExclusivityTheory
}

# Poziom 9: Dziewięć Domen Świata (Domain Profiles)
DOMAINS = {
    "industrial": ["identity", "exclusivity", "gravity", "synergy"],
    "medical": ["psyche", "noos", "synergy"],
    "legal": ["identity", "psyche", "noos"],
    "it_support": ["identity", "logic", "gravity"],
    "creative": ["psyche", "noos"],
    "administrative": ["stability", "decay"],
    "scientific": ["noos", "stability", "synergy"],
    "personal": ["psyche", "decay"],
    "security": ["identity", "entropy", "stability"]
}

def get_theory_by_id(theory_id: str) -> Type[IMathematicalTheory] | None:
    """Helper to find theory in any level of the 3-6-9 hierarchy."""
    all_theories = {**MODULATORS}
    return all_theories.get(theory_id)
