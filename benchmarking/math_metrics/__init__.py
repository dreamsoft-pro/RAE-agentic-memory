"""
RAE Mathematical Metrics Module

Three-tier mathematical model for agent memory analysis:
1. Structure Metrics - geometry of memory (graph connectivity, coherence, entropy)
2. Dynamics Metrics - evolution over time (drift, retention, reflection gain)
3. Policy Metrics - decision optimization (retrieval quality, cost-quality frontier)

This module provides research-grade mathematical analysis tools for RAE benchmarks.
"""

from .structure_metrics import (
    GraphConnectivityScore,
    SemanticCoherenceScore,
    GraphEntropyMetric,
    StructuralDriftMetric,
)
from .dynamics_metrics import (
    MemoryDriftIndex,
    RetentionCurve,
    ReflectionGainScore,
    CompressionFidelityRatio,
)
from .policy_metrics import (
    OptimalRetrievalRatio,
    CostQualityFrontier,
    ReflectionPolicyEfficiency,
)
from .base import MathMetricBase, MemorySnapshot

__all__ = [
    # Base classes
    "MathMetricBase",
    "MemorySnapshot",
    # Structure metrics
    "GraphConnectivityScore",
    "SemanticCoherenceScore",
    "GraphEntropyMetric",
    "StructuralDriftMetric",
    # Dynamics metrics
    "MemoryDriftIndex",
    "RetentionCurve",
    "ReflectionGainScore",
    "CompressionFidelityRatio",
    # Policy metrics
    "OptimalRetrievalRatio",
    "CostQualityFrontier",
    "ReflectionPolicyEfficiency",
]

__version__ = "1.0.0"
