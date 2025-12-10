"""Evaluator component for Reflection V2.

The Evaluator assesses the quality and outcomes of actions.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from rae_core.interfaces.storage import IMemoryStorage
from rae_core.math.metrics import (
    CoherenceMetric,
    CompletenessMetric,
    EntropyMetric,
    RelevanceMetric,
    calculate_quality_score,
)


class Evaluator:
    """Evaluator component that assesses memory quality and action outcomes.

    Implements the "Evaluate" phase of the Actor-Evaluator-Reflector pattern.
    """

    def __init__(
        self,
        memory_storage: IMemoryStorage,
    ):
        """Initialize Evaluator.

        Args:
            memory_storage: Memory storage for retrieval
        """
        self.memory_storage = memory_storage
        self.coherence_metric = CoherenceMetric()
        self.entropy_metric = EntropyMetric()
        self.relevance_metric = RelevanceMetric()
        self.completeness_metric = CompletenessMetric()

    async def evaluate_memory_quality(
        self,
        memory_id: UUID,
        tenant_id: str,
        context: Optional[str] = None,
    ) -> Dict[str, float]:
        """Evaluate quality of a single memory.

        Args:
            memory_id: Memory identifier
            tenant_id: Tenant identifier
            context: Optional context for relevance evaluation

        Returns:
            Dictionary of quality metrics
        """
        memory = await self.memory_storage.get_memory(memory_id, tenant_id)
        if not memory:
            return {"error": 1.0}

        content = memory.get("content", "")
        tokens = content.split()

        metrics = {
            "coherence": self.coherence_metric.compute(content),
            "entropy": self.entropy_metric.compute(tokens),
            "completeness": self.completeness_metric.compute(memory),
        }

        if context:
            metrics["relevance"] = self.relevance_metric.compute(content, context)

        # Calculate overall quality
        metrics["quality"] = calculate_quality_score(metrics)

        return metrics

    async def evaluate_action_outcome(
        self,
        action_type: str,
        action_result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Evaluate the outcome of an action.

        Args:
            action_type: Type of action executed
            action_result: Result from action execution
            context: Original action context

        Returns:
            Evaluation result with success metrics
        """
        if not action_result.get("success"):
            return {
                "outcome": "failure",
                "score": 0.0,
                "reason": action_result.get("error", "Unknown error"),
            }

        # Evaluate based on action type
        if action_type == "consolidate_memories":
            return self._evaluate_consolidation(action_result, context)
        elif action_type == "update_importance":
            return self._evaluate_importance_update(action_result, context)
        elif action_type == "create_semantic_link":
            return self._evaluate_link_creation(action_result, context)
        elif action_type == "prune_duplicates":
            return self._evaluate_pruning(action_result, context)
        else:
            return {
                "outcome": "success",
                "score": 0.5,
                "reason": "Unknown action type",
            }

    def _evaluate_consolidation(
        self,
        result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Evaluate memory consolidation."""
        consolidated_count = result.get("consolidated_count", 0)

        if consolidated_count < 2:
            score = 0.3  # Low value if few memories consolidated
        elif consolidated_count < 5:
            score = 0.7
        else:
            score = 1.0  # High value for many memories

        return {
            "outcome": "success",
            "score": score,
            "reason": f"Consolidated {consolidated_count} memories",
            "metrics": {
                "consolidated_count": consolidated_count,
            }
        }

    def _evaluate_importance_update(
        self,
        result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Evaluate importance score updates."""
        updated_count = result.get("updated_count", 0)
        total = result.get("total", 0)

        if total == 0:
            score = 0.0
        else:
            score = updated_count / total

        return {
            "outcome": "success",
            "score": score,
            "reason": f"Updated {updated_count}/{total} importance scores",
            "metrics": {
                "success_rate": score,
            }
        }

    def _evaluate_link_creation(
        self,
        result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Evaluate semantic link creation."""
        link = result.get("link", {})

        return {
            "outcome": "success",
            "score": 0.8,  # Fixed score for successful link
            "reason": f"Created {link.get('type', 'link')} between memories",
            "metrics": {
                "link_type": link.get("type"),
            }
        }

    def _evaluate_pruning(
        self,
        result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Evaluate memory pruning."""
        pruned_count = result.get("pruned_count", 0)
        total = result.get("total", 0)

        if total == 0:
            score = 0.0
        else:
            score = pruned_count / total

        return {
            "outcome": "success",
            "score": score,
            "reason": f"Pruned {pruned_count}/{total} memories",
            "metrics": {
                "pruning_rate": score,
            }
        }

    async def evaluate_memory_batch(
        self,
        memory_ids: List[UUID],
        tenant_id: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Evaluate quality of multiple memories.

        Args:
            memory_ids: List of memory identifiers
            tenant_id: Tenant identifier
            context: Optional context for relevance

        Returns:
            Aggregated quality metrics
        """
        total_metrics = {
            "coherence": 0.0,
            "entropy": 0.0,
            "completeness": 0.0,
            "quality": 0.0,
        }

        if context:
            total_metrics["relevance"] = 0.0

        count = 0
        for memory_id in memory_ids:
            metrics = await self.evaluate_memory_quality(memory_id, tenant_id, context)
            if "error" not in metrics:
                for key in total_metrics:
                    if key in metrics:
                        total_metrics[key] += metrics[key]
                count += 1

        # Average
        if count > 0:
            for key in total_metrics:
                total_metrics[key] /= count

        return {
            "evaluated_count": count,
            "total": len(memory_ids),
            "metrics": total_metrics,
        }
