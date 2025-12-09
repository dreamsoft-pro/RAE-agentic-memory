"""
Query analyzer for intent detection and query enhancement.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class QueryIntent(str, Enum):
    """Detected query intent."""

    FACTUAL = "factual"  # "What is X?"
    PROCEDURAL = "procedural"  # "How to do X?"
    TEMPORAL = "temporal"  # "When did X happen?"
    COMPARISON = "comparison"  # "What's the difference between X and Y?"
    LIST = "list"  # "List all X"
    RECENT = "recent"  # "What's new/recent about X?"
    PATTERN = "pattern"  # "What patterns in X?"


class AnalyzedQuery(BaseModel):
    """Result of query analysis."""

    original_query: str
    intent: QueryIntent
    keywords: List[str]
    entities: List[str]
    filters: Dict[str, Any]
    enhanced_query: str
    confidence: float


class QueryAnalyzer:
    """
    Analyzes queries to extract intent, keywords, and filters.

    This is a simple rule-based analyzer. In production, this could
    use NLP/LLM for more sophisticated analysis.
    """

    def __init__(self):
        """Initialize query analyzer."""
        self.intent_patterns = {
            QueryIntent.FACTUAL: ["what is", "define", "explain", "tell me about"],
            QueryIntent.PROCEDURAL: ["how to", "how do i", "how can i", "steps to"],
            QueryIntent.TEMPORAL: ["when", "what time", "date"],
            QueryIntent.COMPARISON: ["difference between", "compare", "vs", "versus"],
            QueryIntent.LIST: ["list", "show all", "give me all"],
            QueryIntent.RECENT: ["recent", "latest", "new", "last"],
            QueryIntent.PATTERN: ["pattern", "trend", "common", "similar"],
        }

    async def analyze(self, query: str) -> AnalyzedQuery:
        """
        Analyze query to extract intent and enhance it.

        Args:
            query: Original query text

        Returns:
            Analyzed query with intent, keywords, filters
        """
        query_lower = query.lower()

        # Detect intent
        intent = self._detect_intent(query_lower)

        # Extract keywords
        keywords = self._extract_keywords(query_lower)

        # Extract entities (simple: capitalized words)
        entities = self._extract_entities(query)

        # Build filters based on intent
        filters = self._build_filters(query_lower, intent)

        # Enhance query
        enhanced_query = self._enhance_query(query, intent, keywords)

        # Calculate confidence
        confidence = self._calculate_confidence(query_lower, intent, keywords)

        return AnalyzedQuery(
            original_query=query,
            intent=intent,
            keywords=keywords,
            entities=entities,
            filters=filters,
            enhanced_query=enhanced_query,
            confidence=confidence
        )

    def _detect_intent(self, query_lower: str) -> QueryIntent:
        """Detect query intent based on patterns."""
        for intent, patterns in self.intent_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                return intent

        # Default to factual
        return QueryIntent.FACTUAL

    def _extract_keywords(self, query_lower: str) -> List[str]:
        """Extract important keywords from query."""
        # Remove stop words
        stop_words = {
            "what", "is", "the", "a", "an", "and", "or", "but", "in", "on", "at",
            "to", "for", "of", "with", "by", "from", "about", "how", "when", "where",
            "who", "which", "that", "this", "these", "those", "i", "me", "my",
            "you", "your", "we", "us", "our", "do", "does", "did", "can", "could",
            "would", "should", "may", "might", "will", "shall", "tell", "show",
            "give", "find", "get", "make", "take"
        }

        words = query_lower.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        return keywords

    def _extract_entities(self, query: str) -> List[str]:
        """Extract named entities (capitalized words)."""
        words = query.split()
        entities = [w for w in words if w[0].isupper() and len(w) > 1]
        return entities

    def _build_filters(
        self,
        query_lower: str,
        intent: QueryIntent
    ) -> Dict[str, Any]:
        """Build search filters based on query and intent."""
        filters = {}

        # Temporal filters
        if intent == QueryIntent.RECENT or "recent" in query_lower:
            filters["sort_by"] = "recency"

        # Importance filters
        if "important" in query_lower or "critical" in query_lower:
            filters["min_importance"] = 0.7

        return filters

    def _enhance_query(
        self,
        query: str,
        intent: QueryIntent,
        keywords: List[str]
    ) -> str:
        """Enhance query with synonyms and related terms."""
        # For now, just return the original query
        # In production, this could add synonyms, related terms, etc.
        return query

    def _calculate_confidence(
        self,
        query_lower: str,
        intent: QueryIntent,
        keywords: List[str]
    ) -> float:
        """Calculate confidence in the analysis."""
        confidence = 0.5  # Base confidence

        # Boost if intent pattern matched
        for pattern in self.intent_patterns[intent]:
            if pattern in query_lower:
                confidence += 0.2
                break

        # Boost if we found keywords
        if keywords:
            confidence += min(0.3, len(keywords) * 0.1)

        return min(1.0, confidence)
