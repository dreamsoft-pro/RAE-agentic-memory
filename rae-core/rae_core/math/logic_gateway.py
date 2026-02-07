"""
Logic Gateway - Deterministic Math Core (System 4.0).
Implements logic-based retrieval control instead of continuous weights.
Based on docs/poprawa.txt
"""

from enum import Enum
from typing import Any, Dict, List, Tuple
from uuid import UUID
import structlog

logger = structlog.get_logger(__name__)

class SearchProfile(Enum):
    LEXICAL_FIRST = "lexical_first"
    VECTOR_FIRST = "vector_first"
    CONSENSUS = "consensus"

class LogicGateway:
    """
    Deterministic controller for hybrid search fusion.
    Uses margins and thresholds to select the authoritative source.
    """

    def __init__(self, thresholds: Dict[str, float] | None = None):
        self.thresholds = thresholds or {
            "v_high": 0.15,  # High confidence vector margin
            "t_high": 0.20,  # High confidence text margin (normalized)
            "query_short": 5, # Tokens
            "keyword_density": 0.5
        }

    def route(self, query: str, strategy_results: Dict[str, List[Tuple[UUID, float]]]) -> SearchProfile:
        """
        Route query to a specific profile based on query features and result margins.
        """
        # 1. Analyze query
        tokens = query.split()
        is_short = len(tokens) <= self.thresholds["query_short"]
        
        # Simple heuristic for "industrial" query (logs, IDs)
        has_special = any(not c.isalnum() and not c.isspace() for c in query)
        has_numbers = any(c.isdigit() for c in query)
        is_lexical_candidate = is_short or has_special or has_numbers

        # 2. Calculate Margins
        margins = self._calculate_margins(strategy_results)
        v_margin = margins.get("vector", 0.0)
        t_margin = margins.get("fulltext", 0.0)

        # 3. Decision Logic (Deterministic)
        if is_lexical_candidate and t_margin >= self.thresholds["t_high"]:
            return SearchProfile.LEXICAL_FIRST
        
        if v_margin >= self.thresholds["v_high"] and t_margin < 0.05:
            return SearchProfile.VECTOR_FIRST
            
        if t_margin >= 0.5: # Extreme lexical confidence (Exact match)
            return SearchProfile.LEXICAL_FIRST

        # Default to consensus if no source is clearly dominant or if they disagree
        return SearchProfile.CONSENSUS

    def fuse(self, profile: SearchProfile, strategy_results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """
        Apply the selected profile to fuse results.
        """
        if profile == SearchProfile.LEXICAL_FIRST:
            # Text decides, Vector is auxiliary (fill the gaps)
            return self._fuse_lexical_first(strategy_results)
        
        elif profile == SearchProfile.VECTOR_FIRST:
            # Vector decides, Text is anchor
            return self._fuse_vector_first(strategy_results)
        
        else: # CONSENSUS
            # Use overlap-preferring fusion
            return self._fuse_consensus(strategy_results)

    def _calculate_margins(self, strategy_results: Dict[str, List[Tuple[UUID, float]]]) -> Dict[str, float]:
        """
        Margin = Score(top1) - Score(top2)
        Results are assumed to be normalized [0, 1].
        """
        margins = {}
        for name, results in strategy_results.items():
            if len(results) < 2:
                margins[name] = 1.0 if results else 0.0
                continue
            
            # Confidence Gap
            margin = float(results[0][1]) - float(results[1][1])
            margins[name] = margin
        return margins

    def _fuse_lexical_first(self, results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """LEXICAL-FIRST: Text results take priority."""
        text_results = results.get("fulltext", [])
        vector_results = results.get("vector", [])
        
        # Primary: Text
        fused = {id: score + 10.0 for id, score in text_results} # Huge boost for text
        
        # Auxiliary: Vector
        for id, score in vector_results:
            if id in fused:
                fused[id] += score
            else:
                fused[id] = score
                
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)

    def _fuse_vector_first(self, results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """VECTOR-FIRST: Semantic results take priority."""
        text_results = results.get("fulltext", [])
        vector_results = results.get("vector", [])
        
        # Primary: Vector
        fused = {id: score + 10.0 for id, score in vector_results}
        
        # Anchor: Text
        for id, score in text_results:
            if id in fused:
                fused[id] += score
            else:
                fused[id] = score
                
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)

    def _fuse_consensus(self, results: Dict[str, List[Tuple[UUID, float]]]) -> List[Tuple[UUID, float]]:
        """CONSENSUS: Prefer overlap and resonance."""
        fused: Dict[UUID, float] = {}
        
        strategy_count = len(results)
        for strategy_name, res_list in results.items():
            for id, score in res_list:
                # Resonance boost: if item appears in multiple strategies, it gets multiplied
                if id in fused:
                    fused[id] = (fused[id] + score) * 1.5 
                else:
                    fused[id] = score
                    
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)
