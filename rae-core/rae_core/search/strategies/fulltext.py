"""Full-text keyword search strategy."""

from typing import Any
from uuid import UUID

from rae_core.interfaces.storage import IMemoryStorage
from rae_core.search.strategies import SearchStrategy


class FullTextStrategy(SearchStrategy):
    """Full-text keyword matching search.

    Simple exact and partial keyword matching for fast retrieval.
    Useful for tag-based and exact phrase searches.
    """

    def __init__(
        self,
        memory_storage: IMemoryStorage,
        default_weight: float = 0.05,
    ):
        """Initialize full-text strategy.

        Args:
            memory_storage: Memory storage for content retrieval
            default_weight: Default weight in hybrid search (0.0-1.0)
        """
        self.memory_storage = memory_storage
        self.default_weight = default_weight

    def _normalize(self, text: str) -> str:
        """Normalize text for matching."""
        return text.lower().strip()

    def _compute_match_score(
        self,
        query: str,
        content: str,
        tags: list[str],
    ) -> float:
        """Compute match score based on keyword presence."""
        if query == "*":
            return 1.0

        query_norm = self._normalize(query)
        content_norm = self._normalize(content)
        tags_norm = [self._normalize(tag) for tag in tags]

        score = 0.0

        if query_norm in content_norm:
            score += 1.0
        if query_norm in tags_norm:
            score += 0.8

        query_words = set(query_norm.split())
        content_words = set(content_norm.split())
        tag_words = set(word for tag in tags_norm for word in tag.split())

        content_overlap = (
            len(query_words & content_words) / len(query_words) if query_words else 0
        )
        tag_overlap = (
            len(query_words & tag_words) / len(query_words) if query_words else 0
        )

        score += content_overlap * 0.6
        score += tag_overlap * 0.4

        return min(score, 1.0)

    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
        project: str | None = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float, float]]:
        """Execute full-text search.

        Returns:
            List of (memory_id, match_score, importance) tuples
        """
        layer = filters.get("layer") if filters else None
        agent_id = filters.get("agent_id") if filters else None
        project = project or (filters.get("project") if filters else None)

        # SYSTEM 9.0: Check for strict mode in kwargs (passed from Controller/Engine)
        gateway_config = kwargs.get("gateway_config", {})
        is_strict = gateway_config.get("confidence_gate", 0.0) >= 0.95
        
        # We pass 'strict_mode' via filters or query modification?
        # Ideally, IMemoryStorage.list_memories should support search_type.
        # Since we can't change the interface easily, we append a signal to the query 
        # OR we rely on the implementation of list_memories to handle complex queries.
        
        # HACK: If strict, we assume the user wants ALL terms.
        # In 'websearch_to_tsquery', quoting terms forces AND.
        # So we quote the query if strict mode is active.
        search_query = query
        if is_strict and '"' not in query:
             search_query = f'"{query}"'

        memories = await self.memory_storage.list_memories(
            tenant_id=tenant_id,
            agent_id=agent_id,
            layer=layer,
            limit=limit,
            project=project,
            filters=filters,
            query=search_query, # Modified query for strictness
        )

        if not memories:
            return []

        results: list[tuple[UUID, float, float]] = []
        for memory in memories:
            memory_id = memory["id"]
            if isinstance(memory_id, str):
                memory_id = UUID(memory_id)

            score = memory.get("rank") or memory.get("score")

            if score is None:
                score = self._compute_match_score(
                    query=query, # Score against original query
                    content=memory.get("content", ""),
                    tags=memory.get("tags", []),
                )

            score = float(score)
            importance = float(memory.get("importance", 0.0))

            if score > 0:
                results.append((memory_id, score, importance))

        return results

    def get_strategy_name(self) -> str:
        return "fulltext"

    def get_strategy_weight(self) -> float:
        return self.default_weight
