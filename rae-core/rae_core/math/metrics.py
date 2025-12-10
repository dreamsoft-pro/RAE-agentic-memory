"""Metrics for memory quality assessment."""

from typing import Any, Dict, List
import math


class CoherenceMetric:
    """Measures logical coherence of memory content."""

    def compute(self, content: str) -> float:
        """Compute coherence score (0-1)."""
        # Simple heuristic: longer coherent text scores higher
        words = content.split()
        if len(words) < 3:
            return 0.3
        return min(1.0, len(words) / 100.0 + 0.5)


class EntropyMetric:
    """Measures information entropy."""

    def compute(self, tokens: List[str]) -> float:
        """Compute Shannon entropy of token distribution."""
        if not tokens:
            return 0.0

        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1

        total = len(tokens)
        entropy = 0.0
        for count in freq.values():
            p = count / total
            entropy -= p * math.log2(p) if p > 0 else 0

        # Normalize to 0-1 range
        max_entropy = math.log2(len(freq)) if freq else 1.0
        return entropy / max_entropy if max_entropy > 0 else 0.0


class RelevanceMetric:
    """Measures relevance to context."""

    def compute(self, memory: str, context: str) -> float:
        """Compute relevance score."""
        memory_words = set(memory.lower().split())
        context_words = set(context.lower().split())

        if not memory_words or not context_words:
            return 0.0

        overlap = len(memory_words & context_words)
        return overlap / len(memory_words)


class CompletenessMetric:
    """Measures information completeness."""

    def compute(self, memory: Dict[str, Any]) -> float:
        """Score based on presence of key fields."""
        required_fields = ['content', 'source', 'timestamp']
        optional_fields = ['tags', 'metadata', 'context']

        required_score = sum(1 for f in required_fields if memory.get(f)) / len(required_fields)
        optional_score = sum(1 for f in optional_fields if memory.get(f)) / len(optional_fields)

        return required_score * 0.7 + optional_score * 0.3


# Utility functions
def calculate_quality_score(metrics: Dict[str, float]) -> float:
    """Aggregate multiple metrics into single quality score."""
    if not metrics:
        return 0.5

    weights = {
        'coherence': 0.25,
        'relevance': 0.30,
        'completeness': 0.25,
        'entropy': 0.20
    }

    score = sum(metrics.get(k, 0.5) * w for k, w in weights.items())
    return min(1.0, max(0.0, score))
