"""Math Layer Controller - orchestrates all mathematical operations."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import structlog

from rae_core.math.bandit.bandit import BanditConfig, MultiArmedBandit
from rae_core.math.dynamics import calculate_recency_score
from rae_core.math.features_v2 import FeaturesV2
from rae_core.math.policy import compute_memory_score
from rae_core.math.structure import ScoringWeights, cosine_similarity
from rae_core.math.types import TaskType

logger = structlog.get_logger(__name__)


class MathLayerController:
    """
    Controller for RAE math layer operations.

    Orchestrates:
    - Importance calculations
    - Decay functions
    - Similarity scoring
    - Online policy tuning (Bandit)
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize controller with optional config."""
        self.config = config or {}

        # Initialize Bandit for Online Learning
        # Default persistence path
        if isinstance(self.config, dict):
            persist_path = self.config.get("bandit_persistence_path")
            exploration_rate = self.config.get("exploration_rate", 0.1)
        else:
            persist_path = getattr(self.config, "bandit_persistence_path", None)
            exploration_rate = getattr(self.config, "exploration_rate", 0.1)

        if not persist_path:
            # Fallback to local file
            persist_path = Path("bandit_state.json")

        bandit_config = BanditConfig(
            persistence_path=Path(persist_path), exploration_rate=exploration_rate
        )
        self.bandit = MultiArmedBandit(config=bandit_config)

        # Internal state for tracking active decisions
        self._last_decision: dict[str, Any] = {}

    def get_weights(self, query: str, active_strategies: list[str]) -> dict[str, float]:
        """Alias for get_retrieval_weights with strategy awareness."""
        base_weights = self.get_retrieval_weights(query)

        # Ensure all active strategies have a weight
        final_weights = {}
        for name in active_strategies:
            final_weights[name] = base_weights.get(name, 1.0)

        return final_weights

    def get_retrieval_weights(
        self, query: str, context: dict | None = None
    ) -> dict[str, float]:
        """
        Determine optimal retrieval weights (FullText vs Vector) using Bandit.

        Args:
            query: The search query string
            context: Additional context (memory count, etc.)

        Returns:
            Dict with 'fulltext' and 'vector' weights.
        """
        # 1. Build features from context
        features = self._build_features(query, context)

        # 2. Select Arm from Bandit
        # Note: The existing Bandit select_arm returns (Arm, was_exploration)
        # We use Arm.strategy to determine weights.
        arm, was_explore = self.bandit.select_arm(features)

        # 3. Map Arm Strategy to Weights
        # Implementation of System 3.0 logic
        strategy = arm.strategy

        if strategy.startswith("w_txt"):
            # Parse weights from name: w_txt10p0_vec1p0 -> txt=10.0, vec=1.0
            try:
                import re
                match = re.match(r"w_txt([\dp]+)_vec([\dp]+)", strategy)
                if match:
                    txt_w = float(match.group(1).replace("p", "."))
                    vec_w = float(match.group(2).replace("p", "."))
                    weights = {"fulltext": txt_w, "vector": vec_w}
                else:
                    weights = {"fulltext": 1.0, "vector": 1.0}
            except Exception as e:
                logger.error("weight_parsing_failed", strategy=strategy, error=str(e))
                weights = {"fulltext": 1.0, "vector": 1.0}
        elif strategy == "relevance_scoring":  # Favour Vector
            weights = {"fulltext": 0.5, "vector": 2.0}
        elif strategy == "importance_scoring":  # Favour Text
            weights = {"fulltext": 2.0, "vector": 0.5}
        else:  # Default/Balanced
            weights = {"fulltext": 1.0, "vector": 1.0}

        # Track decision for later update
        self._last_decision = {
            "arm": arm,
            "features": features,
            "timestamp": datetime.now(timezone.utc),
            "weights": weights,
        }

        return weights

    def get_resonance_threshold(self, query: str) -> float:
        """
        Determine Szubar (Resonance) Threshold using Bandit context.
        
        Logic:
        - Factual Query (High Text Weight) -> High Threshold (0.8-0.9) [Conservative]
        - Abstract Query (High Vector Weight) -> Low Threshold (0.3-0.4) [Aggressive]
        """
        # Reuse decision if available for this request cycle
        if self._last_decision:
            weights = self._last_decision.get("weights", {})
            txt_w = weights.get("fulltext", 1.0)
            vec_w = weights.get("vector", 1.0)
            
            # Simple heuristic mapping
            if txt_w > vec_w * 2: # Strongly Factual
                return 0.85
            elif vec_w > txt_w * 2: # Strongly Abstract
                return 0.35
            else:
                return 0.6 # Balanced
        
        # Fallback if no decision yet (shouldn't happen in standard flow)
        return 0.6

    def update_policy(self, success: bool, reward: float = 1.0):
        """
        Update bandit policy based on search success.
        """
        if not self._last_decision:
            return

        arm = self._last_decision["arm"]
        features = self._last_decision["features"]

        # Observation reward
        obs_reward = reward if success else 0.0

        self.bandit.update(arm, obs_reward, features)
        self._last_decision = {}  # Clear

    def _build_features(self, query: str, context: dict | None = None) -> FeaturesV2:
        """Helper to build FeaturesV2 from raw data."""
        ctx = context or {}
        return FeaturesV2(
            task_type=TaskType.MEMORY_RETRIEVE,
            memory_count=ctx.get("memory_count", 0),
            graph_density=ctx.get("graph_density", 0.0),
            memory_entropy=ctx.get("memory_entropy", 0.0),
            query_complexity=len(query.split()) / 20.0,  # Simple proxy
        )

    def score_memory(
        self,
        memory: dict[str, Any],
        query_similarity: float = 0.5,
        weights: Any | None = None,
    ) -> float:
        """Score a memory's importance with optional weights."""
        # Handle missing created_at
        created_at = memory.get("created_at")
        if created_at is None:
            created_at = datetime.now(timezone.utc)

        # Use weights from param, or from last decision if relevant, or default
        active_weights = weights
        if active_weights is None:
            # We could use alpha/beta/gamma tuning here too
            active_weights = ScoringWeights()

        result = compute_memory_score(
            similarity=query_similarity,
            importance=memory.get("importance", 0.5),
            last_accessed_at=memory.get("last_accessed_at"),
            created_at=created_at,  # type: ignore
            access_count=memory.get("usage_count", 0),
            weights=active_weights,
        )
        return float(result.final_score)

    def apply_decay(self, age_hours: float, usage_count: int = 0) -> float:
        """Apply time-based decay to importance."""
        from datetime import timedelta

        now = datetime.now(timezone.utc)
        created_at = now - timedelta(hours=age_hours)

        score, _, _ = calculate_recency_score(
            last_accessed_at=None,
            created_at=created_at,
            access_count=usage_count,
            now=now,
        )
        return float(score)

    def compute_similarity(
        self, embedding1: list[float], embedding2: list[float]
    ) -> float:
        """Compute cosine similarity between embeddings."""
        try:
            return cosine_similarity(embedding1, embedding2)
        except Exception:
            import math

            dot = sum(a * b for a, b in zip(embedding1, embedding2))
            mag1 = math.sqrt(sum(a * a for a in embedding1))
            mag2 = math.sqrt(sum(b * b for b in embedding2))
            return dot / (mag1 * mag2) if (mag1 * mag2) > 0 else 0.0
