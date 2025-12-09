"""
Search module for RAE-Core.

Provides various search strategies and hybrid search capabilities.
"""

from rae_core.search.engine import SearchEngine
from rae_core.search.fusion import FusionStrategy, score_fusion
from rae_core.search.query_analyzer import QueryAnalyzer

__all__ = [
    "SearchEngine",
    "FusionStrategy",
    "score_fusion",
    "QueryAnalyzer",
]
