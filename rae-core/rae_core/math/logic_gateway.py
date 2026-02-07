"""
Logic Gateway - Deterministic Math Core (System 6.4).
Implements Resonance Cascade and Confidence Gates.
"""

from enum import Enum
from typing import Any, Dict, List, Tuple
from uuid import UUID
import structlog
from .semantic_resonance import SemanticResonance

logger = structlog.get_logger(__name__)

class SearchProfile(Enum):
    LEXICAL_FIRST = "lexical_first"
    VECTOR_FIRST = "vector_first"
    CONSENSUS = "consensus"

class LogicGateway:
    """
    Deterministic controller for hybrid search fusion.
    Uses Semantic Resonance and Confidence Gates (Early Exit).
    """

    def __init__(self, thresholds: Dict[str, float] | None = None):
        self.thresholds = thresholds or {
            "v_high": 0.15,
            "t_high": 0.20,
            "confidence_gate": 0.9, # Early exit threshold
            "resonance_low": 0.35,  # Threshold for Specific/Lexical
            "resonance_high": 0.70, # Threshold for Abstract/Vector
            "rrf_k": 10             # Tighter ranking for Top-1 priority
        }
        self.resonance_calculator = SemanticResonance()

    def route(self, query: str, strategy_results: Dict[str, List[Tuple[UUID, float]]]) -> SearchProfile:
        """
        Route query based on Semantic Resonance and Confidence Gates.
        """
        # 1. Calculate Resonance (System 6.4)
        resonance = self.resonance_calculator.calculate(query)
        
        # 2. Check for Immediate Lexical Confidence (Gatekeeper)
        # If we already have results (from a pre-check) and they are perfect, stay Lexical.
        t_results = strategy_results.get("fulltext", [])
        if t_results and self._is_high_confidence(t_results[0][1]):
            return SearchProfile.LEXICAL_FIRST

        # 3. Resonance-based Routing
        if resonance < self.thresholds["resonance_low"]:
            # Low resonance = Specific (IDs, Errors, Code) -> Lexical Priority
            return SearchProfile.LEXICAL_FIRST
        
        if resonance > self.thresholds["resonance_high"]:
             # High resonance = Abstract -> Vector Priority
            return SearchProfile.VECTOR_FIRST

        # Default to consensus
        return SearchProfile.CONSENSUS

    def fuse(self, profile: SearchProfile, strategy_results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """
        Apply the selected profile to fuse results with Early Exit logic.
        """
        fused_results: List[Tuple[UUID, float]] = []
        
        if profile == SearchProfile.LEXICAL_FIRST:
            fused_results = self._fuse_lexical_first(strategy_results)
        elif profile == SearchProfile.VECTOR_FIRST:
            fused_results = self._fuse_vector_first(strategy_results)
        else: # CONSENSUS
            fused_results = self._fuse_consensus(strategy_results)
            
        return self._apply_resonance(fused_results, strategy_results)

    def _is_high_confidence(self, score: float) -> bool:
        """Check if a score passes the Confidence Gate."""
        # Assuming Postgres/Vector scores are somewhat normalized or distinct
        # For Postgres, exact matches often have arbitrary high scores, but we assume 
        # normalized behavior or distinct magnitude for this logic.
        # In this implementation, we treat > 0.9 as 'Perfect'.
        return score >= self.thresholds["confidence_gate"]

    def _apply_resonance(self, fused_list: List[Tuple[UUID, float]], strategy_results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """
        Resonance: If a result appears in multiple independent strategies, boost it.
        """
        fused_map = dict(fused_list)
        vector_ranks = {id: idx for idx, (id, _) in enumerate(strategy_results.get("vector", []))}
        text_ranks = {id: idx for idx, (id, _) in enumerate(strategy_results.get("fulltext", []))}
        
        final_scores = {}
        for id in fused_map:
            v_rank = vector_ranks.get(id, 9999)
            t_rank = text_ranks.get(id, 9999)
            
            # Boost logic: If consistent across engines
            if v_rank < 50 and t_rank < 50:
                final_scores[id] = fused_map[id] * 1.5 
            else:
                final_scores[id] = fused_map[id]

        return sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    def _calculate_margins(self, strategy_results: Dict[str, List[Tuple[UUID, float]]]) -> Dict[str, float]:
        margins = {}
        for name, results in strategy_results.items():
            if len(results) < 2:
                margins[name] = 1.0 if results else 0.0
                continue
            margin = float(results[0][1]) - float(results[1][1])
            margins[name] = margin
        return margins

    def _fuse_lexical_first(self, results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """LEXICAL-FIRST: Check for Early Exit, then RRF."""
        text_results = results.get("fulltext", [])
        
        # EARLY EXIT CRITERIA (System 6.5 Hybrid Resilience):
        # Only exit early if:
        # 1. We have results.
        # 2. The top result is high confidence.
        # 3. AND the result set is small (specific). 
        #    If we have > 5 results, it's likely a generic keyword match (e.g. "error") 
        #    and we NEED vectors/RRF to rank the relevant specific entry to the top.
        is_specific_enough = len(text_results) <= 5
        
        if text_results and self._is_high_confidence(text_results[0][1]) and is_specific_enough:
            # Return just the lexical list (no pollution from vector)
            return text_results

        # Fallback to RRF with Lexical Priority
        vector_results = {id: idx for idx, (id, _) in enumerate(results.get("vector", []))}
        merged = {}
        k = self.thresholds["rrf_k"]
        
        for idx, (id, score) in enumerate(text_results):
            # Base score from rank (1/rank)
            rrf_score = 1.0 / (idx + k)
            
            # Vector bonus if present
            if id in vector_results:
                v_rank = vector_results[id]
                rrf_score += 1.0 / (v_rank + k)
            merged[id] = rrf_score + 10.0 # Maintain dominance
                
        return sorted(merged.items(), key=lambda x: x[1], reverse=True)

    def _fuse_vector_first(self, results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """VECTOR-FIRST: Semantic priority."""
        vector_results = results.get("vector", [])
        
        # EARLY EXIT (Rare for vectors, but possible with high threshold)
        if vector_results and vector_results[0][1] > 0.95: 
             return vector_results

        text_ranks = {id: idx for idx, (id, _) in enumerate(results.get("fulltext", []))}
        fused = {}
        k = self.thresholds["rrf_k"]
        
        for idx, (id, score) in enumerate(vector_results):
            rrf_score = 1.0 / (idx + k)
            if id in text_ranks:
                rrf_score += 1.0 / (text_ranks[id] + k)
            fused[id] = rrf_score + 10.0
                
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)

    def _fuse_consensus(self, results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """CONSENSUS: Pure RRF Fusion (Tighter k)."""
        fused: Dict[UUID, float] = {}
        k = self.thresholds["rrf_k"]
        
        for strategy_name, res_list in results.items():
            for rank, (id, _) in enumerate(res_list):
                score = 1.0 / (rank + k)
                if id in fused:
                    fused[id] += score
                else:
                    fused[id] = score
                    
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)
