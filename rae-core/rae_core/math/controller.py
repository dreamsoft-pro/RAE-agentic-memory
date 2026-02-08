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
        if isinstance(self.config, dict):
            persist_path = self.config.get("bandit_persistence_path")
            exploration_rate = self.config.get("exploration_rate", 0.1)
        else:
            persist_path = getattr(self.config, "bandit_persistence_path", None)
            exploration_rate = getattr(self.config, "exploration_rate", 0.1)

        if not persist_path:
            persist_path = Path("bandit_state.json")

        bandit_config = BanditConfig(
            persistence_path=Path(persist_path), exploration_rate=exploration_rate
        )
        self.bandit = MultiArmedBandit(config=bandit_config)

        # Internal state for tracking active decisions
        self._last_decision: dict[str, Any] = {}

    def get_engine_param(self, key: str, default: Any = None) -> Any:
        """Retrieve an externalized engine parameter."""
        params = (
            self.config.get("engine_params", {})
            if isinstance(self.config, dict)
            else {}
        )
        return params.get(key, default)

    def get_agnostic_weights(
        self, query: str, results_map: dict[str, list[tuple[Any, float]]]
    ) -> dict[str, float]:
        """
        Dynamically determine weights for vector spaces based on Signal-to-Noise Ratio (SNR).
        A 'spike' in scores indicates signal. Flat distributions indicate noise.
        """
        weights = {}
        for space, results in results_map.items():
            if not results:
                weights[space] = 0.0
                continue

            scores = [r[1] for r in results]
            if len(scores) < 2:
                weights[space] = 1.0
                continue

            # Calculate SNR: (Max - Mean) / StdDev
            mean_score = sum(scores) / len(scores)
            max_score = max(scores)
            std_dev = (sum((s - mean_score) ** 2 for s in scores) / len(scores)) ** 0.5

            snr = (max_score - mean_score) / (std_dev + 0.0001)

            # Intelligence: If SNR is high, this space has a clear winner.
            weights[space] = 1.0 + (snr * 2.0)

            # Prioritize known quality spaces
            if space == "nomic":
                weights[space] *= 2.0
            if space == "dense" and snr < 2.0:  # MiniLM is noisy
                weights[space] *= 0.5

        return weights

    def get_weights(self, query: str, active_strategies: list[str]) -> dict[str, float]:
        """Alias for get_retrieval_weights with strategy awareness."""
        base_weights = self.get_retrieval_weights(query)

        final_weights = {}
        for name in active_strategies:
            final_weights[name] = base_weights.get(name, 1.0)

        return final_weights

    def get_retrieval_weights(
        self, query: str, context: dict | None = None
    ) -> dict[str, float]:
        """
        Determine optimal retrieval weights (FullText vs Vector).
        """
        # 0. Check if Bandit is enabled in config
        bandit_enabled = False
        if isinstance(self.config, dict):
            bandit_enabled = self.config.get(
                "bandit_enabled", True
            )  # Default to True for synergy
        else:
            bandit_enabled = getattr(self.config, "bandit_enabled", True)

        if not bandit_enabled:
            strategy = self.config.get("fixed_strategy", "default")
            features = self._build_features(query, context)
            arm = None
        else:
            # 1. Build features from context
            features = self._build_features(query, context)

            # 2. Select Arm from Bandit
            arm, was_explore = self.bandit.select_arm(features)
            strategy = arm.strategy

        # 3. Map Arm Strategy to Weights
        # SYSTEM 12.0: Smarter Oracle Seeding
        weights = {"fulltext": 1.0}
        txt_w, vec_w = 1.0, 1.0

        # Refined Industrial Detection: High Density + Specific Tokens or High Keyword Ratio
        has_log_tokens = any(t in query.lower() for t in ["[err", "log_", "uuid", "0x"])
        is_industrial = (
            features.term_density > 0.9 and features.keyword_ratio > 0.15
        ) or has_log_tokens

        if strategy == "default" or strategy.startswith("hybrid_default"):
            if is_industrial:
                # Log/Code pattern detected -> Heavy Bias towards Text (The Oracle Seed)
                txt_w, vec_w = 10.0, 1.0
            else:
                # Natural Language -> Balanced start
                txt_w, vec_w = 1.0, 1.0

        elif strategy.startswith("w_txt"):
            try:
                import re

                match = re.match(r"w_txt([\dp]+)_vec([\dp]+)", strategy)
                if match:
                    txt_w = float(match.group(1).replace("p", "."))
                    vec_w = float(match.group(2).replace("p", "."))
            except Exception:
                pass
        elif strategy == "relevance_scoring":
            txt_w, vec_w = 0.5, 2.0
        elif strategy == "importance_scoring":
            txt_w, vec_w = 2.0, 0.5

        weights["fulltext"] = txt_w
        weights["vector"] = vec_w

        # Track decision for feedback update
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
        """
        # Get baseline from config
        baseline = float(self.get_engine_param("szubar_induction_energy", 0.8))

        if self._last_decision:
            weights = self._last_decision.get("weights", {})
            txt_w = weights.get("fulltext", 1.0)
            vec_w = weights.get("vector", 1.0)

            # More aggressive resonance for hybrid/abstract queries
            if (
                vec_w > txt_w * 1.5
            ):  # Strongly Abstract -> Very Aggressive (Low Threshold)
                return 0.25
            elif (
                txt_w > vec_w * 1.5
            ):  # Strongly Factual -> Conservative (High Threshold)
                return baseline  # Use configured conservative limit
            else:
                return 0.45

        return 0.45

    def update_policy(self, success: bool, reward: float = 1.0):
        """
        Update bandit policy based on search success.
        """
        if not self._last_decision or not self._last_decision.get("arm"):
            return

        arm = self._last_decision["arm"]
        features = self._last_decision["features"]
        obs_reward = reward if success else 0.0

        self.bandit.update(arm, obs_reward, features)
        self._last_decision = {}

    def _build_features(self, query: str, context: dict | None = None) -> FeaturesV2:
        """Helper to build FeaturesV2 from raw data."""
        ctx = context or {}

        # Analyze query structure
        terms = query.split()
        total_tokens = len(terms)
        unique_terms = len(set(terms))
        term_density = unique_terms / total_tokens if total_tokens > 0 else 0.0

        special_chars = sum(1 for c in query if not c.isalnum() and not c.isspace())
        capitalized = sum(1 for t in terms if t[0].isupper()) if terms else 0
        keyword_ratio = (special_chars + capitalized) / len(query) if query else 0.0

        return FeaturesV2(
            task_type=TaskType.MEMORY_RETRIEVE,
            memory_count=ctx.get("memory_count", 0),
            graph_density=ctx.get("graph_density", 0.0),
            memory_entropy=ctx.get("memory_entropy", 0.0),
            query_complexity=len(terms) / 20.0,
            term_density=term_density,
            keyword_ratio=keyword_ratio,
        )

    def score_memory(
        self,
        memory: dict[str, Any],
        query_similarity: float = 0.5,
        weights: Any | None = None,
    ) -> float:
        """Score a memory's importance with optional weights."""
        created_at = memory.get("created_at")
        if created_at is None:
            created_at = datetime.now(timezone.utc)

        active_weights = weights or ScoringWeights()

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
