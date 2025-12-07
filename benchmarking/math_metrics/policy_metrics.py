"""
Policy Metrics - Decision Optimization

These metrics analyze the quality of memory policy decisions:
- Optimal Retrieval Ratio (ORR): How often optimal memories are retrieved
- Cost-Quality Frontier (CQF): Trade-off between cost and quality
- Reflection Policy Efficiency: Whether reflection was triggered appropriately
"""

from typing import Dict, List, Tuple, Any, Set

import numpy as np

from .base import MathMetricBase


class OptimalRetrievalRatio(MathMetricBase):
    """
    Optimal Retrieval Ratio (ORR)

    Measures how often the system retrieves optimal memory fragments.

    Formula: ORR = optimal_hits / total_retrievals

    We define "optimal" as memories that:
    1. Are in the ground truth for the query
    2. Are ranked in top-k results

    High ORR = system consistently retrieves best memories
    Low ORR = system retrieves suboptimal memories

    Range: 0.0 (never optimal) to 1.0 (always optimal)
    Typical good value: > 0.7
    """

    def __init__(self):
        super().__init__(
            name="optimal_retrieval_ratio",
            description="Frequency of optimal memory retrieval",
        )

    def calculate(
        self,
        query_results: List[Dict[str, Any]],
        k: int = 5,
    ) -> float:
        """
        Calculate ORR from query results.

        Args:
            query_results: List of query result dicts with 'expected' and 'retrieved' keys
            k: Top-k threshold

        Returns:
            ORR value (0.0 to 1.0)
        """
        if len(query_results) == 0:
            self._last_value = 0.0
            self._last_metadata = {
                "num_queries": 0,
                "reason": "No queries provided",
            }
            return 0.0

        optimal_hits = 0
        total_queries = len(query_results)

        # Track detailed stats
        rank_positions = []  # Position of first relevant result
        num_optimal_per_query = []

        for result in query_results:
            expected = set(result.get("expected", []))
            retrieved = result.get("retrieved", [])[:k]

            # Count how many optimal results in top-k
            optimal_count = sum(1 for mem_id in retrieved if mem_id in expected)
            num_optimal_per_query.append(optimal_count)

            # Mark as hit if at least one optimal result in top-k
            if optimal_count > 0:
                optimal_hits += 1

                # Find rank of first optimal result
                for i, mem_id in enumerate(retrieved, 1):
                    if mem_id in expected:
                        rank_positions.append(i)
                        break

        orr = optimal_hits / total_queries

        self._last_value = orr
        self._last_metadata = {
            "num_queries": total_queries,
            "optimal_hits": optimal_hits,
            "k": k,
            "avg_rank_of_first_hit": (
                float(np.mean(rank_positions)) if rank_positions else 0.0
            ),
            "avg_optimal_per_query": float(np.mean(num_optimal_per_query)),
        }

        return orr


class CostQualityFrontier(MathMetricBase):
    """
    Cost-Quality Frontier (CQF)

    Measures the trade-off between reflection cost and quality improvement.

    Formula: CQF = reflection_gain / tokens_used * 1000

    This gives us "quality improvement per 1000 tokens".

    High CQF = efficient reflection (good quality for low cost)
    Low CQF = inefficient reflection (small improvement for high cost)

    Range: Unbounded (can be negative if reflection degrades quality)
    Typical good value: > 0.01 (1% quality improvement per 1000 tokens)
    """

    def __init__(self):
        super().__init__(
            name="cost_quality_frontier",
            description="Quality improvement per unit cost",
        )

    def calculate(
        self,
        reflection_gain: float,
        tokens_used: int,
    ) -> float:
        """
        Calculate CQF from reflection results.

        Args:
            reflection_gain: Quality improvement (RG score)
            tokens_used: Total tokens consumed

        Returns:
            CQF value (quality per 1000 tokens)
        """
        if tokens_used == 0:
            self._last_value = 0.0
            self._last_metadata = {
                "reflection_gain": reflection_gain,
                "tokens_used": 0,
                "reason": "No tokens used",
            }
            return 0.0

        # Calculate efficiency: gain per 1000 tokens
        cqf = (reflection_gain / tokens_used) * 1000

        self._last_value = cqf
        self._last_metadata = {
            "reflection_gain": reflection_gain,
            "tokens_used": tokens_used,
            "cost_efficiency": "high" if cqf > 0.01 else "medium" if cqf > 0.005 else "low",
        }

        return cqf


class ReflectionPolicyEfficiency(MathMetricBase):
    """
    Reflection Policy Efficiency

    Measures whether reflection was triggered at the right times.

    We analyze:
    1. True Positives: Reflection triggered when needed (gain > threshold)
    2. False Positives: Reflection triggered but no benefit
    3. True Negatives: No reflection when not needed
    4. False Negatives: Missed opportunities (should have reflected but didn't)

    Efficiency = (TP + TN) / (TP + TN + FP + FN)

    Range: 0.0 (poor policy) to 1.0 (perfect policy)
    Typical good value: > 0.8
    """

    def __init__(self):
        super().__init__(
            name="reflection_policy_efficiency",
            description="Accuracy of reflection trigger decisions",
        )

    def calculate(
        self,
        reflection_events: List[Dict[str, Any]],
        gain_threshold: float = 0.05,
    ) -> float:
        """
        Calculate policy efficiency.

        Args:
            reflection_events: List of events with:
                - 'triggered': bool (was reflection triggered)
                - 'gain': float (actual reflection gain)
                - 'needed': bool (was reflection needed based on gain threshold)
            gain_threshold: Minimum gain to consider reflection "needed"

        Returns:
            Efficiency score (0.0 to 1.0)
        """
        if len(reflection_events) == 0:
            self._last_value = 0.0
            self._last_metadata = {
                "num_events": 0,
                "reason": "No reflection events provided",
            }
            return 0.0

        # Count policy outcomes
        true_positives = 0  # Triggered and beneficial
        false_positives = 0  # Triggered but not beneficial
        true_negatives = 0  # Not triggered and not needed
        false_negatives = 0  # Not triggered but was needed

        for event in reflection_events:
            triggered = event.get("triggered", False)
            gain = event.get("gain", 0.0)
            needed = gain >= gain_threshold

            if triggered and needed:
                true_positives += 1
            elif triggered and not needed:
                false_positives += 1
            elif not triggered and not needed:
                true_negatives += 1
            elif not triggered and needed:
                false_negatives += 1

        total = len(reflection_events)
        efficiency = (true_positives + true_negatives) / total if total > 0 else 0.0

        # Calculate precision and recall for reflection policy
        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )
        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        self._last_value = efficiency
        self._last_metadata = {
            "num_events": total,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "true_negatives": true_negatives,
            "false_negatives": false_negatives,
            "precision": precision,
            "recall": recall,
            "gain_threshold": gain_threshold,
        }

        return efficiency
