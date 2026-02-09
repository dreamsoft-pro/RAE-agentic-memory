"""
Math Layer Controller - The Brain of RAE.
Manages the selection of mathematical strategies (L1/L2/L3) and weights using Multi-Armed Bandit.
"""

import math
import os
from typing import Any, Dict, List, Optional
from uuid import UUID

import numpy as np
import structlog

from rae_core.math.bandit.bandit import MultiArmedBandit, BanditConfig
from rae_core.math.features_v2 import FeatureExtractorV2
from rae_core.math.structure import ScoringWeights
from rae_core.math.bandit.arm import Arm
from rae_core.math.types import MathLevel

logger = structlog.get_logger(__name__)


class MathLayerController:
    """
    Controller that decides HOW to search/score based on query features.
    Uses a Contextual Bandit to select from a 'Spectrum' of strategies.
    """

    def __init__(self, config: dict[str, Any] | Any | None = None):
        self.config = config or {}
        
        # Normalize Pydantic model to dict
        if hasattr(self.config, "model_dump"):
            self.config = self.config.model_dump()
        elif hasattr(self.config, "dict"):
            self.config = self.config.dict()
            
        self.feature_extractor = FeatureExtractorV2()
        
        # Initialize Bandit with 'Spectrum' Arms
        self.bandit = self._initialize_spectrum_bandit()
        self._last_selected_arm = None

    def _initialize_spectrum_bandit(self) -> MultiArmedBandit:
        """Generates spectrum of arms."""
        arms = []
        
        def create_arm(name, weights, params):
            arm = Arm(level=MathLevel.L1, strategy=name)
            arm.config = {"weights": weights, "params": params}
            return arm

        # 1. Hybrid Arms
        for i in range(11):
            ratio = i / 10.0
            weights = {
                "fulltext": round(1.0 - ratio, 2) * 10,
                "vector": max(0.5, round(ratio, 2) * 10), # Floor at 0.5 to keep semantic search alive
                "anchor": 1000.0,
            }
            params = {"resonance_factor": 0.2, "rerank_gate": 0.5, "rerank_limit": 300}
            arms.append(create_arm(f"hybrid_{ratio:.1f}", weights, params))

        # 2. Resonance Arms
        for i in range(1, 11):
            factor = round(i * 0.2, 2)
            weights = {"fulltext": 5.0, "vector": 5.0, "anchor": 1000.0}
            params = {"resonance_factor": factor, "rerank_gate": 0.3, "rerank_limit": 300}
            arms.append(create_arm(f"resonance_{factor:.1f}", weights, params))

        # 3. Strict Arms
        for i in range(5):
            threshold = round(0.5 + (i * 0.1), 2)
            weights = {"fulltext": 20.0, "vector": 0.1, "anchor": 1000.0}
            params = {"resonance_factor": 0.0, "rerank_gate": threshold, "rerank_limit": 300}
            arms.append(create_arm(f"strict_{threshold:.1f}", weights, params))

        # 4. Abstract Arms
        for i in range(5):
            vec_w = 10.0 + (i * 5.0)
            weights = {"fulltext": 1.0, "vector": vec_w, "anchor": 50.0}
            params = {"resonance_factor": 1.5, "rerank_gate": 0.1}
            arms.append(create_arm(f"abstract_{i}", weights, params))

        bandit_conf = self.config.get("bandit")
        conf_obj = BanditConfig(**bandit_conf) if bandit_conf else BanditConfig()
        return MultiArmedBandit(config=conf_obj, arms=arms)

    def get_retrieval_weights(self, query: str) -> Dict[str, Any]:
        """Selects weights based on query context."""
        features = self.feature_extractor.extract(query)
        selected_arm, _ = self.bandit.select_arm(features)
        self._last_selected_arm = selected_arm
        
        # 3. Dynamic Rerank Limit (No Hardcoding)
        derived = features.compute_derived_features()
        m_scale = derived.get("memory_scale", 0.0)
        e_scale = derived.get("entropy_normalized", 0.0)
        
        dynamic_limit = int(50 + (250 * m_scale) + (50 * e_scale))
        
        # Update logger with REAL dynamic limit
        logger.info("math_strategy_selected", 
                    arm=selected_arm.arm_id, 
                    industrial=features.is_industrial, 
                    weights=selected_arm.config["weights"],
                    dynamic_limit=dynamic_limit)
        
        result = selected_arm.config["weights"].copy()
        result["_params"] = selected_arm.config["params"].copy()
        
        # Use arm's limit or fallback to dynamic
        if "rerank_limit" not in result["_params"]:
            result["_params"]["rerank_limit"] = dynamic_limit
            
        result["_arm_id"] = selected_arm.arm_id
        return result

    def score_memory(
        self,
        memory: Dict[str, Any],
        query_similarity: float,
        weights: ScoringWeights | None = None,
    ) -> float:
        """Compute Math Score."""
        alpha, beta, gamma = 0.4, 0.3, 0.3
        if weights:
            alpha, beta, gamma = weights.alpha, weights.beta, weights.gamma
        sim = float(np.clip(query_similarity, 0.0, 1.0))
        imp = float(np.clip(memory.get("importance", 0.5), 0.0, 1.0))
        score = (alpha * sim) + (beta * imp) + (gamma * 1.0)
        return float(np.clip(score, 0.0, 1.0))

    def get_engine_param(self, key: str, default: Any) -> Any:
        # Dynamic Scaling for Retrieval Limit
        if key == "limit":
            # For 100k memories, we need limit ~500. For 1k ~200.
            # Scale based on features (use cached if available or re-extract)
            # Since we don't have query here, we use a global memory scale if possible
            # or just a generous default for large datasets.
            return self.config.get("engine_params", {}).get(key, 300)
        return self.config.get("engine_params", {}).get(key, default)

    def get_resonance_threshold(self, query: str) -> float:
        return 0.5

    def update_policy(self, success: bool, query: str = "", **kwargs) -> None:
        """Update policy with rank-based reward."""
        if not self.config.get("bandit", {}).get("enabled", True):
            return
        reward = 0.0
        if success:
            rank = kwargs.get("rank", 1)
            reward = 1.0 / float(rank)
        logger.info("policy_update_received", success=success, reward=reward, rank=kwargs.get("rank"))
        features = self.feature_extractor.extract(query)
        if self._last_selected_arm:
            self.bandit.update(self._last_selected_arm, reward, features)