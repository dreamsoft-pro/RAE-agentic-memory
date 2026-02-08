"""
Logic Gateway - Deterministic Math Core (System 11.2 - Adaptive Noise Floor).
Implements dynamic waterfall thresholds based on result density to balance 
Small-Scale Precision (0.5 threshold) vs Large-Scale Noise (0.8 threshold).
"""

from enum import Enum
from typing import Any, Dict, List, Tuple, Union
from uuid import UUID
import structlog
from .semantic_resonance import SemanticResonance

logger = structlog.get_logger(__name__)

# Type for strategy results: List of (UUID, score, optional_importance)
StrategyResult = List[Union[Tuple[UUID, float], Tuple[UUID, float, float]]]

class SearchProfile(Enum):
    LEXICAL_FIRST = "lexical_first"
    VECTOR_FIRST = "vector_first"
    CONSENSUS = "consensus"

class LogicGateway:
    """
    Adaptive controller using Density-Aware Waterfall Clipping and Scale-Aware RRF.
    """

    def __init__(self, thresholds: Dict[str, float] | None = None):
        self.default_thresholds = thresholds or {
            "v_high": 0.15,
            "t_high": 0.20,
            "confidence_gate": 0.9, 
            "resonance_low": 0.35,  
            "resonance_high": 0.70, 
            "rrf_k_base": 20             
        }
        self.resonance_calculator = SemanticResonance()

    def route(self, query: str, strategy_results: Dict[str, StrategyResult]) -> SearchProfile:
        resonance = self.resonance_calculator.calculate(query)
        t_results = strategy_results.get("fulltext", [])
        
        if t_results and t_results[0][1] >= self.default_thresholds["confidence_gate"] and len(t_results) < 5:
            return SearchProfile.LEXICAL_FIRST
            
        if resonance < self.default_thresholds["resonance_low"]:
            return SearchProfile.LEXICAL_FIRST
        if resonance > self.default_thresholds["resonance_high"]:
            return SearchProfile.VECTOR_FIRST
        return SearchProfile.CONSENSUS

    def fuse(
        self, 
        profile: SearchProfile, 
        strategy_results: Dict[str, StrategyResult], 
        weights: Dict[str, float] | None = None,
        query: str = "",
        config_override: Dict[str, float] | None = None
    ) -> List[Tuple[UUID, float]]:
        active_config = self.default_thresholds.copy()
        if config_override: active_config.update(config_override)

        # 1. NORMALIZATION & CONFIDENCE-AWARE WATERFALL FILTERING (System 12.0)
        normalized_results = self._normalize_and_clip_adaptive(strategy_results, weights)

        # 2. CALCULATE ADAPTIVE K
        total_count = sum(len(res) for res in normalized_results.values())
        adaptive_k = max(active_config["rrf_k_base"], min(250.0, total_count / 10.0))
        active_config["rrf_k"] = adaptive_k

        fused_results: List[Tuple[UUID, float]] = []
        if profile == SearchProfile.LEXICAL_FIRST:
            fused_results = self._fuse_lexical_first(normalized_results, active_config)
        elif profile == SearchProfile.VECTOR_FIRST:
            fused_results = self._fuse_vector_first(normalized_results, active_config)
        else:
            fused_results = self._fuse_consensus(normalized_results, active_config)
            
        return self._apply_resonance(fused_results, normalized_results, profile)

    def _normalize_and_clip_adaptive(
        self, 
        strategy_results: Dict[str, StrategyResult],
        weights: Dict[str, float] | None = None
    ) -> Dict[str, List[Tuple[UUID, float, float]]]:
        """
        SYSTEM 12.1: Oracle Resilience (Lenient Clipping).
        """
        normalized = {}
        weights = weights or {"fulltext": 1.0, "vector": 1.0}
        
        # Check for Lexical Confidence (The Oracle Gate)
        t_results = strategy_results.get("fulltext", [])
        has_high_lexical_confidence = (
            t_results and 
            t_results[0][1] >= self.default_thresholds["confidence_gate"]
        )

        for engine, res_list in strategy_results.items():
            if not res_list:
                normalized[engine] = []
                continue
                
            std_list = []
            for item in res_list:
                if len(item) == 3: std_list.append(item)
                else: std_list.append((item[0], item[1], 0.0))
            
            max_score = std_list[0][1]
            raw_count = len(res_list)
            
            if engine == "fulltext":
                # Text is sparse, baseline threshold 0.3
                threshold_ratio = 0.3
            else:
                # Vector density: 0.3 (Small) -> 0.5 (Med) -> 0.7 (Large)
                if raw_count < 50:
                    threshold_ratio = 0.3
                elif raw_count < 300:
                    threshold_ratio = 0.5
                else:
                    threshold_ratio = 0.7
                
                # SYSTEM 12.1 V-CLIP:
                # High-pressure pruning if lexical hit is confirmed.
                if has_high_lexical_confidence:
                    threshold_ratio = max(threshold_ratio, 0.85)
                    logger.info("oracle_vclip_activated", engine=engine, new_ratio=threshold_ratio)

            threshold = max_score * threshold_ratio
            clipped = [r for r in std_list if r[1] >= threshold]
            
            # Safety: Keep at least Top-10
            if len(clipped) < 10 and len(std_list) >= 10:
                clipped = std_list[:10]
            elif not clipped:
                clipped = std_list[:1]
                
            normalized[engine] = clipped
            
        return normalized

    def _apply_resonance(
        self, 
        fused_list: List[Tuple[UUID, float]], 
        results: Dict[str, List[Tuple[UUID, float, float]]],
        profile: SearchProfile = SearchProfile.CONSENSUS
    ) -> List[Tuple[UUID, float]]:
        """
        Final stage processing with Oracle Synergy (System 12.1).
        """
        fused_map = dict(fused_list)
        v_ranks = {id: idx for idx, (id, _, _) in enumerate(results.get("vector", []))}
        t_ranks = {id: idx for idx, (id, _, _) in enumerate(results.get("fulltext", []))}
        
        importance_map = {}
        for res_list in results.values():
            for id, _, imp in res_list:
                importance_map[id] = max(importance_map.get(id, 0.0), imp)

        final_scores = {}
        for id in fused_map:
            v_rank = v_ranks.get(id, 999)
            t_rank = t_ranks.get(id, 999)
            score = fused_map[id]
            
            # SYSTEM 12.1 ORACLE SYNERGY:
            # Massive boost for cross-engine confirmation
            if v_rank < 50 and t_rank < 50:
                multiplier = 3.0 if profile == SearchProfile.LEXICAL_FIRST else 2.0
                score *= multiplier
                
            # Content-Aware Bonus (Importance)
            score += importance_map.get(id, 0.0) * 0.01 
            final_scores[id] = score
            
        return sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    def _fuse_lexical_first(self, results: Dict[str, List[Tuple[UUID, float, float]]], config: Dict[str, float]) -> List[Tuple[UUID, float]]:
        text_results = results.get("fulltext", [])
        vector_results = results.get("vector", [])
        v_ranks = {id: idx for idx, (id, _, _) in enumerate(vector_results)}
        
        merged = {}
        k = config["rrf_k"]
        
        # 1. Process Text (Primary)
        for idx, (id, score, _) in enumerate(text_results):
            # SYSTEM 12.0: Oracle Numerator (5.0x boost for lexical positioning)
            rrf = 5.0 / (idx + k)
            if id in v_ranks: 
                rrf += 1.0 / (v_ranks[id] + k)
            merged[id] = rrf + 10.0 # Base boost for being in text
            
        # 2. Process Vectors not in Text (Safety Fallback)
        for idx, (id, score, _) in enumerate(vector_results):
            if id not in merged:
                # Lower boost (no +10.0) ensures text results always win if they exist
                merged[id] = 1.0 / (idx + k)
                
        return sorted(merged.items(), key=lambda x: x[1], reverse=True)

    def _fuse_vector_first(self, results: Dict[str, List[Tuple[UUID, float, float]]], config: Dict[str, float]) -> List[Tuple[UUID, float]]:
        vector_results = results.get("vector", [])
        text_results = results.get("fulltext", [])
        t_ranks = {id: idx for idx, (id, _, _) in enumerate(text_results)}
        
        merged = {}
        k = config["rrf_k"]
        
        # 1. Process Vectors (Primary)
        for idx, (id, score, _) in enumerate(vector_results):
            rrf = 1.0 / (idx + k)
            if id in t_ranks: 
                rrf += 5.0 / (t_ranks[id] + k) # Boost if also in text
            merged[id] = rrf + 10.0
            
        # 2. Process Text not in Vectors
        for idx, (id, score, _) in enumerate(text_results):
            if id not in merged:
                merged[id] = 5.0 / (idx + k) # Text is high signal even if vectors missed it
                
        return sorted(merged.items(), key=lambda x: x[1], reverse=True)

    def _fuse_consensus(self, results: Dict[str, List[Tuple[UUID, float, float]]], config: Dict[str, float]) -> List[Tuple[UUID, float]]:
        """
        Standard RRF with Oracle Synergy (System 12.1).
        """
        fused = {}
        k = config["rrf_k"]
        
        # Track engine appearance for synergy
        appearance = {}

        for engine, res_list in results.items():
            for rank, (id, score, _) in enumerate(res_list):
                # RRF calculation
                weight = 5.0 if engine == "fulltext" else 1.0
                val = weight / (rank + k)
                
                fused[id] = fused.get(id, 0.0) + val
                appearance[id] = appearance.get(id, 0) + 1

        # Apply Consensus Boost
        for id in fused:
            if appearance[id] > 1:
                fused[id] *= 2.0 # Double score if both engines agree
                
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)

    