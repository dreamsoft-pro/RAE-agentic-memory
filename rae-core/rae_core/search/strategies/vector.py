"""Vector-based semantic search strategy."""

from typing import Any
from uuid import UUID

from rae_core.interfaces.embedding import IEmbeddingProvider
from rae_core.interfaces.vector import IVectorStore
from rae_core.search.strategies import SearchStrategy


class VectorSearchStrategy(SearchStrategy):
    """Semantic search using vector embeddings.

    Uses cosine similarity between query embedding and memory embeddings.
    """

    def __init__(
        self,
        vector_store: IVectorStore,
        embedding_provider: IEmbeddingProvider,
        default_weight: float = 0.8,
    ):
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider
        self.default_weight = default_weight

    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
        project: str | None = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float, float]]: # UPDATED RETURN TYPE
        """Execute semantic search.

        Returns:
            List of (memory_id, similarity_score, importance) tuples
        """
        query_embedding = await self.embedding_provider.embed_text(
            query, task_type="search_query"
        )

        _layer = filters.get("layer") if filters else None
        _agent_id = filters.get("agent_id") if filters else None
        project = project or (filters.get("project") if filters else None)
        _session_id = filters.get("session_id") if filters else None
        _score_threshold = filters.get("score_threshold", 0.0) if filters else 0.0

        vector_name = kwargs.get("vector_name") or (
            filters.get("vector_name") if filters else None
        )

        # Assumes vector_store.search_similar returns (UUID, score, metadata) or handles metadata extraction internally
        # BUT standard IVectorStore returns (UUID, float).
        # We need to update QdrantAdapter first? Or rely on IVectorStore update.
        
        # Checking QdrantAdapter implementation (from memory/context):
        # QdrantAdapter.search_similar returns list[tuple[UUID, float]].
        # It internally fetches payload but discards it in the return.
        
        # For now, we will stick to (UUID, score) and return 0.0 importance
        # UNLESS we update QdrantAdapter. This is a deeper change.
        
        results = await self.vector_store.search_similar(
            query_embedding=query_embedding,
            tenant_id=tenant_id,
            limit=limit,
            layer=_layer,
            agent_id=_agent_id,
            session_id=_session_id,
            score_threshold=_score_threshold,
            project=project,
            vector_name=vector_name,
        )

        # Map to 3-tuple
        final_results = []
        for item in results:
            if len(item) == 3:
                final_results.append(item)
            else:
                final_results.append((item[0], item[1], 0.0))

        return final_results

    def get_strategy_name(self) -> str:
        return "vector"

    def get_strategy_weight(self) -> float:
        return self.default_weight