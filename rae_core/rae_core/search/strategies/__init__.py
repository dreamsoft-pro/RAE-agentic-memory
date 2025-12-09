"""
Search strategies for different retrieval approaches.
"""

from rae_core.search.strategies.base import SearchStrategy
from rae_core.search.strategies.keyword import KeywordSearchStrategy
from rae_core.search.strategies.recency import RecencySearchStrategy
from rae_core.search.strategies.importance import ImportanceSearchStrategy

__all__ = [
    "SearchStrategy",
    "KeywordSearchStrategy",
    "RecencySearchStrategy",
    "ImportanceSearchStrategy",
]
