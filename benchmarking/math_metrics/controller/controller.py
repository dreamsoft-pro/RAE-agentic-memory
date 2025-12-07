"""
MathLayerController - Central controller for math level selection

This is the main entry point for deciding which mathematical level
to use for memory operations. It provides:
- Rule-based level selection (Iteration 1)
- Standardized decision format
- Comprehensive logging for future learning
- Integration with existing MathematicalDecisionEngine
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import structlog

from ..decision_engine import MathematicalDecisionEngine
from ..base import MemorySnapshot
from .types import MathLevel, TaskType
from .features import Features
from .decision import MathDecision, DecisionWithOutcome
from .context import TaskContext
from .config import MathControllerConfig


logger = structlog.get_logger(__name__)


class FeatureExtractor:
    """
    Extracts features from TaskContext for decision making.

    Centralizes all feature extraction logic to ensure consistency
    between training and inference (important for Iteration 2+).
    """

    def __init__(self, decision_engine: Optional[MathematicalDecisionEngine] = None):
        """
        Initialize extractor.

        Args:
            decision_engine: Optional decision engine for metric calculations
        """
        self.decision_engine = decision_engine or MathematicalDecisionEngine()

    def extract(self, context: TaskContext) -> Features:
        """
        Extract features from task context.

        Args:
            context: Task context with memory state and metadata

        Returns:
            Features dataclass for decision making
        """
        features = Features(task_type=context.task_type)

        # Extract memory state features
        if context.memory_snapshot:
            features.memory_count = context.memory_snapshot.num_memories

            # Calculate graph density
            num_edges = len(context.memory_snapshot.graph_edges)
            max_edges = features.memory_count * (features.memory_count - 1) / 2
            features.graph_density = num_edges / max_edges if max_edges > 0 else 0.0

        # Extract session features
        features.session_length = context.turn_number

        # Extract budget constraints
        features.cost_budget = context.budget_constraints.get("max_cost_usd")
        features.latency_budget_ms = context.budget_constraints.get("max_latency_ms")

        # Calculate metrics if we have snapshots
        if context.memory_snapshot and len(context.memory_snapshot.graph_edges) > 0:
            # Use decision engine metrics
            from ..structure_metrics import GraphEntropyMetric, GraphConnectivityScore, SemanticCoherenceScore

            entropy_metric = GraphEntropyMetric()
            gcs_metric = GraphConnectivityScore()
            scs_metric = SemanticCoherenceScore()

            features.memory_entropy = entropy_metric.calculate(
                num_nodes=context.memory_snapshot.num_memories,
                edges=context.memory_snapshot.graph_edges,
            )
            features.recent_gcs = gcs_metric.calculate(
                num_nodes=context.memory_snapshot.num_memories,
                edges=context.memory_snapshot.graph_edges,
            )
            features.recent_scs = scs_metric.calculate(context.memory_snapshot)

        # Calculate MRR from query results
        if context.query_results:
            from ..policy_metrics import OptimalRetrievalRatio
            orr_metric = OptimalRetrievalRatio()
            features.recent_mrr = orr_metric.calculate(context.query_results, k=5)

        return features


class MathLayerController:
    """
    Central controller for math level selection in RAE.

    This controller is responsible for:
    1. Deciding which math level (L1, L2, L3) to use
    2. Selecting specific strategies within each level
    3. Configuring parameters for the selected strategy
    4. Logging decisions for future learning

    Iteration 1 Focus:
    - Clean, rule-based decision logic
    - Standardized MathDecision output
    - Comprehensive logging
    - Integration with existing systems

    Usage:
        controller = MathLayerController()

        context = TaskContext(
            task_type=TaskType.MEMORY_RETRIEVE,
            memory_snapshot=snapshot,
        )

        decision = controller.decide(context)

        print(f"Using {decision.selected_level} with {decision.strategy_id}")
        print(f"Reason: {decision.explanation}")
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        config: Optional[MathControllerConfig] = None,
    ):
        """
        Initialize the controller.

        Args:
            config_path: Path to YAML config file
            config: Config object (takes precedence over config_path)
        """
        # Load configuration
        if config:
            self.config = config
        elif config_path:
            from .config import load_config
            self.config = load_config(config_path)
        else:
            self.config = MathControllerConfig()  # Default config

        # Initialize components
        self.decision_engine = MathematicalDecisionEngine(
            thresholds=self.config.thresholds
        )
        self.feature_extractor = FeatureExtractor(self.decision_engine)

        # Decision history (in-memory, for recent decisions)
        self.decision_history: List[MathDecision] = []
        self._max_history = 1000

        # Previous decision (for stability)
        self._previous_decision: Optional[MathDecision] = None

        logger.info(
            "math_layer_controller_initialized",
            profile=self.config.profile,
            default_level=self.config.default_level.value,
        )

    def decide(self, context: TaskContext) -> MathDecision:
        """
        Make a decision about which math level to use.

        This is the main entry point for the controller.

        Args:
            context: Task context with all relevant information

        Returns:
            MathDecision with selected level, strategy, params, and explanation
        """
        # Extract features
        features = self.feature_extractor.extract(context)

        # Add history to features
        if self._previous_decision:
            features.previous_level = self._previous_decision.selected_level
            # Note: previous_level_success would be set after outcome is known

        # Select level
        level = self.select_level(features)

        # Select strategy within level
        strategy = self.select_strategy(level, features)

        # Configure parameters
        params = self.configure_params(level, strategy, features)

        # Build explanation
        explanation = self._build_explanation(level, strategy, features)

        # Create decision
        decision = MathDecision(
            selected_level=level,
            strategy_id=strategy,
            params=params,
            explanation=explanation,
            telemetry_tags=self._build_telemetry_tags(level, strategy, features, context),
            features_used=features,
            confidence=self._calculate_confidence(level, features),
        )

        # Log and store
        self.log_decision(decision)
        self._store_decision(decision)

        return decision

    def select_level(self, features: Features) -> MathLevel:
        """
        Select which math level to use based on features.

        Iteration 1 Logic (Rule-based):
        1. If budget-constrained -> L1 (cheapest)
        2. If latency-constrained -> L1 (fastest)
        3. If task prefers L2 AND conditions met -> L2
        4. If high-value scenario AND profile allows -> L3
        5. Default to configured default

        Args:
            features: Extracted features from context

        Returns:
            Selected MathLevel
        """
        # Rule 1: Budget constraint forces L1
        if features.is_budget_constrained():
            logger.debug("level_selection_budget_constrained", level="L1")
            return MathLevel.L1

        # Rule 2: Latency constraint forces L1
        if features.is_latency_constrained():
            logger.debug("level_selection_latency_constrained", level="L1")
            return MathLevel.L1

        # Rule 3: Check if L3 is appropriate (high-value scenarios)
        if self._should_use_l3(features):
            logger.debug("level_selection_high_value", level="L3")
            return MathLevel.L3

        # Rule 4: Check if L2 is appropriate
        if self._should_use_l2(features):
            logger.debug("level_selection_l2_conditions_met", level="L2")
            return MathLevel.L2

        # Rule 5: Use task's preferred level
        preferred = features.task_type.preferred_level
        if self._is_level_allowed(preferred):
            logger.debug("level_selection_task_preferred", level=preferred.value)
            return preferred

        # Default
        return self.config.default_level

    def _should_use_l3(self, features: Features) -> bool:
        """Check if L3 (adaptive/hybrid) should be used"""
        # L3 conditions (Iteration 1: conservative)
        if not self._is_level_allowed(MathLevel.L3):
            return False

        # Only use L3 for complex scenarios
        is_complex_task = features.task_type in [
            TaskType.REFLECTION_DEEP,
            TaskType.MEMORY_CONSOLIDATE,
        ]

        # Large memory count suggests need for sophisticated handling
        has_large_memory = features.memory_count > self.config.thresholds.get(
            "l3_memory_threshold", 500
        )

        # Long session suggests established context
        has_long_session = features.session_length > self.config.thresholds.get(
            "l3_session_threshold", 10
        )

        return is_complex_task and (has_large_memory or has_long_session)

    def _should_use_l2(self, features: Features) -> bool:
        """Check if L2 (information-theoretic) should be used"""
        if not self._is_level_allowed(MathLevel.L2):
            return False

        # L2 is good for tasks that benefit from entropy analysis
        l2_preferred_tasks = [
            TaskType.MEMORY_CONSOLIDATE,
            TaskType.REFLECTION_DEEP,
            TaskType.GRAPH_UPDATE,
            TaskType.CONTEXT_SELECT,
        ]

        if features.task_type in l2_preferred_tasks:
            # Use L2 if we have enough data to make it worthwhile
            has_sufficient_data = features.memory_count > self.config.thresholds.get(
                "l2_memory_threshold", 50
            )
            return has_sufficient_data

        # Also use L2 if entropy is high (disorganized memory)
        high_entropy = features.memory_entropy > self.config.thresholds.get(
            "l2_entropy_threshold", 0.7
        )

        return high_entropy and features.memory_count > 20

    def _is_level_allowed(self, level: MathLevel) -> bool:
        """Check if level is allowed in current config"""
        return level in self.config.allowed_levels

    def select_strategy(self, level: MathLevel, features: Features) -> str:
        """
        Select specific strategy within the chosen level.

        Args:
            level: Selected math level
            features: Extracted features

        Returns:
            Strategy identifier string
        """
        available_strategies = self.config.strategies.get(level, ["default"])

        if level == MathLevel.L1:
            # L1 strategies based on task type
            if features.task_type == TaskType.MEMORY_RETRIEVE:
                return "relevance_scoring"
            elif features.task_type == TaskType.MEMORY_STORE:
                return "importance_scoring"
            else:
                return "default"

        elif level == MathLevel.L2:
            # L2 strategies
            if features.memory_entropy > 0.6:
                return "entropy_minimization"
            elif features.task_type == TaskType.CONTEXT_SELECT:
                return "information_bottleneck"
            else:
                return "mutual_information"

        elif level == MathLevel.L3:
            # L3 strategies (Iteration 1: just default)
            return "hybrid_default"

        return "default"

    def configure_params(
        self,
        level: MathLevel,
        strategy: str,
        features: Features,
    ) -> Dict[str, Any]:
        """
        Configure parameters for the selected strategy.

        Args:
            level: Selected math level
            strategy: Selected strategy
            features: Extracted features

        Returns:
            Dictionary of parameters for the strategy
        """
        base_params = self.config.strategy_params.get(strategy, {}).copy()

        # Adjust based on features
        if level == MathLevel.L1:
            base_params.update({
                "use_recency": True,
                "recency_weight": self._calculate_recency_weight(features),
                "importance_threshold": self.config.thresholds.get(
                    "importance_threshold", 0.3
                ),
            })

        elif level == MathLevel.L2:
            base_params.update({
                "entropy_target": 0.5,
                "ib_beta": self._calculate_ib_beta(features),
                "max_iterations": 100,
            })

        elif level == MathLevel.L3:
            base_params.update({
                "l1_weight": 0.5,
                "l2_weight": 0.5,
                "exploration_rate": 0.1 if self.config.profile == "research" else 0.0,
            })

        return base_params

    def _calculate_recency_weight(self, features: Features) -> float:
        """Calculate recency weight based on session length"""
        # Longer sessions should weight recency less
        if features.session_length < 5:
            return 0.3
        elif features.session_length < 20:
            return 0.2
        else:
            return 0.1

    def _calculate_ib_beta(self, features: Features) -> float:
        """Calculate Information Bottleneck beta parameter"""
        # Higher entropy -> lower beta (more compression)
        # Lower entropy -> higher beta (preserve more info)
        base_beta = 1.0
        entropy_factor = 1.0 - min(features.memory_entropy, 1.0)
        return base_beta * (0.5 + 0.5 * entropy_factor)

    def _build_explanation(
        self,
        level: MathLevel,
        strategy: str,
        features: Features,
    ) -> str:
        """Build human-readable explanation for the decision"""
        parts = []

        # Level explanation
        parts.append(f"Selected {level.value} ({level.description})")

        # Why this level
        if level == MathLevel.L1:
            if features.is_budget_constrained():
                parts.append("Reason: Budget constraints require lowest-cost approach")
            elif features.is_latency_constrained():
                parts.append("Reason: Latency constraints require fastest approach")
            else:
                parts.append(f"Reason: Task type '{features.task_type.value}' works well with L1")

        elif level == MathLevel.L2:
            if features.memory_entropy > 0.6:
                parts.append(f"Reason: High memory entropy ({features.memory_entropy:.2f}) suggests need for information-theoretic optimization")
            else:
                parts.append(f"Reason: Task type '{features.task_type.value}' benefits from entropy analysis")

        elif level == MathLevel.L3:
            parts.append(f"Reason: Complex scenario (memory_count={features.memory_count}, session_length={features.session_length}) benefits from adaptive approach")

        # Strategy explanation
        parts.append(f"Strategy: {strategy}")

        return " | ".join(parts)

    def _build_telemetry_tags(
        self,
        level: MathLevel,
        strategy: str,
        features: Features,
        context: TaskContext,
    ) -> Dict[str, str]:
        """Build telemetry tags for observability"""
        return {
            "math.level": level.value,
            "math.strategy": strategy,
            "math.task_type": features.task_type.value,
            "math.profile": self.config.profile,
            "session.length": str(features.session_length),
            "memory.count": str(features.memory_count),
            "tenant.id": str(context.session_metadata.get("tenant_id", "unknown")),
        }

    def _calculate_confidence(self, level: MathLevel, features: Features) -> float:
        """
        Calculate confidence score for the decision.

        Higher confidence when:
        - Clear constraints force the decision
        - Lots of data supports the choice
        - Previous decisions were successful
        """
        confidence = 0.7  # Base confidence

        # Forced decisions have high confidence
        if features.is_budget_constrained() or features.is_latency_constrained():
            confidence = 0.95

        # More data -> higher confidence
        if features.memory_count > 100:
            confidence += 0.1

        # Previous success -> higher confidence
        if features.previous_level_success is True:
            confidence += 0.1

        return min(confidence, 1.0)

    def log_decision(self, decision: MathDecision) -> None:
        """
        Log decision for analysis and future learning.

        Logs to:
        1. Structured logger (for observability)
        2. Decision log file (for offline analysis)
        """
        # Structured logging
        logger.info(
            "math_decision_made",
            decision_id=decision.decision_id,
            level=decision.selected_level.value,
            strategy=decision.strategy_id,
            confidence=decision.confidence,
            explanation=decision.explanation,
            **decision.telemetry_tags,
        )

        # File logging (if configured)
        if self.config.logging.file_path:
            self._append_to_log_file(decision)

    def _append_to_log_file(self, decision: MathDecision) -> None:
        """Append decision to JSON Lines log file"""
        log_path = Path(self.config.logging.file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, "a") as f:
            f.write(decision.to_json() + "\n")

    def _store_decision(self, decision: MathDecision) -> None:
        """Store decision in history"""
        self.decision_history.append(decision)
        self._previous_decision = decision

        # Trim history if needed
        if len(self.decision_history) > self._max_history:
            self.decision_history = self.decision_history[-self._max_history:]

    def get_decision_history(self, limit: int = 100) -> List[MathDecision]:
        """Get recent decision history"""
        return self.decision_history[-limit:]

    def record_outcome(
        self,
        decision_id: str,
        success: bool,
        metrics: Dict[str, float],
    ) -> Optional[DecisionWithOutcome]:
        """
        Record the outcome of a decision for future learning.

        Args:
            decision_id: ID of the decision
            success: Whether the operation was successful
            metrics: Outcome metrics (e.g., mrr, latency_ms)

        Returns:
            DecisionWithOutcome if decision found, None otherwise
        """
        # Find decision
        decision = None
        for d in reversed(self.decision_history):
            if d.decision_id == decision_id:
                decision = d
                break

        if not decision:
            logger.warning("decision_not_found_for_outcome", decision_id=decision_id)
            return None

        # Create outcome-linked decision
        outcome = decision.with_outcome(success, metrics)

        # Log outcome
        logger.info(
            "math_decision_outcome_recorded",
            decision_id=decision_id,
            success=success,
            metrics=metrics,
        )

        # In Iteration 2+, this would be saved for training
        if self.config.logging.save_outcomes:
            self._save_outcome(outcome)

        return outcome

    def _save_outcome(self, outcome: DecisionWithOutcome) -> None:
        """Save outcome for future learning (Iteration 2+)"""
        outcome_path = Path(self.config.logging.outcome_file_path)
        outcome_path.parent.mkdir(parents=True, exist_ok=True)

        with open(outcome_path, "a") as f:
            f.write(json.dumps(outcome.to_training_example()) + "\n")

    def update_config(self, config: MathControllerConfig) -> None:
        """Update controller configuration at runtime"""
        self.config = config
        self.decision_engine.update_thresholds(config.thresholds)
        logger.info("math_controller_config_updated", profile=config.profile)

    def explain_decision(self, decision: MathDecision) -> str:
        """
        Generate detailed explanation of a decision.

        More verbose than the inline explanation for debugging.
        """
        lines = [
            f"Decision ID: {decision.decision_id}",
            f"Timestamp: {decision.timestamp.isoformat()}",
            f"",
            f"Selected Level: {decision.selected_level.value}",
            f"  Description: {decision.selected_level.description}",
            f"  Cost Multiplier: {decision.selected_level.cost_multiplier}x",
            f"",
            f"Strategy: {decision.strategy_id}",
            f"Parameters: {json.dumps(decision.params, indent=2)}",
            f"",
            f"Explanation: {decision.explanation}",
            f"Confidence: {decision.confidence:.2f}",
            f"",
            f"Features Used:",
        ]

        if decision.features_used:
            for key, value in decision.features_used.to_dict().items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)
