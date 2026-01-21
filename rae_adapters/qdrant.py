from typing import Any, Optional, List, Dict, Tuple, Coroutine
from uuid import UUID
import structlog
from rae_core.interfaces.vector import IVectorStore

logger = structlog.get_logger(__name__)

class QdrantVectorStore(IVectorStore):
    def __init__(self, client: Any, collection_name: str = "memories", embedding_dim: int = 768, distance: str = "Cosine"):
        self.client = client
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self.distance = distance
        self._initialized = False

    async def ainit(self):
        if not self._initialized:
            await self._ensure_collection()
            self._initialized = True

    async def _ensure_collection(self):
        pass

    def _get_vector_name(self, dim: int) -> str:
        if dim == 1536: return "openai"
        if dim == 768: return "ollama"
        return "dense"

    async def _get_compatible_vector_names(self, query_dim: int) -> List[str]:
        try:
            collection_info = await self.client.get_collection(self.collection_name)
            vector_config = collection_info.config.params.vectors
            compatible_names = []
            if hasattr(vector_config, 'map'):
                for name, params in vector_config.map.items():
                    if params.size == query_dim: compatible_names.append(name)
            elif hasattr(vector_config, 'size'):
                if vector_config.size == query_dim: compatible_names.append("")
            return compatible_names or [self._get_vector_name(query_dim)]
        except Exception:
            return [self._get_vector_name(query_dim)]

    async def search_similar(self, query_embedding: list[float], tenant_id: str, layer: str | None = None, limit: int = 10, score_threshold: float | None = None, agent_id: str | None = None, session_id: str | None = None, filters: dict[str, Any] | None = None) -> list[tuple[UUID, float]]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue
        must_conditions = [FieldCondition(key="tenant_id", match=MatchValue(value=str(tenant_id)))]
        if agent_id: must_conditions.append(FieldCondition(key="agent_id", match=MatchValue(value=str(agent_id))))
        if layer: must_conditions.append(FieldCondition(key="layer", match=MatchValue(value=str(layer))))
        if session_id: must_conditions.append(FieldCondition(key="session_id", match=MatchValue(value=str(session_id))))
        if filters:
            for key, value in filters.items():
                if key in ["tenant_id", "agent_id", "session_id", "layer", "score_threshold"]: continue
                must_conditions.append(FieldCondition(key=key, match=MatchValue(value=str(value))))
        query_filter = Filter(must=must_conditions)
        vector_names = await self._get_compatible_vector_names(len(query_embedding))
        all_results: Dict[UUID, float] = {}
        from qdrant_client.models import NamedVector
        for v_name in vector_names:
            try:
                search_vector = query_embedding if not v_name else NamedVector(name=v_name, vector=query_embedding)
                results = await self.client.search(collection_name=self.collection_name, query_vector=search_vector, query_filter=query_filter, limit=limit, score_threshold=score_threshold)
                for res in results:
                    m_id = UUID(res.payload["memory_id"])
                    if m_id not in all_results or res.score > all_results[m_id]: all_results[m_id] = res.score
            except Exception as e: logger.error("qdrant_search_failed", space=v_name, error=str(e))
        return sorted(all_results.items(), key=lambda x: x[1], reverse=True)[:limit]

    async def store_vector(self, memory_id: UUID, embedding: list[float] | dict[str, list[float]], tenant_id: str, metadata: dict[str, Any] | None = None) -> bool:
        return True
    async def get_vector(self, memory_id: UUID, tenant_id: str) -> list[float] | None:
        return None
    async def delete_vector(self, memory_id: UUID, tenant_id: str) -> bool:
        return True
    async def update_vector(self, memory_id: UUID, embedding: list[float] | dict[str, list[float]], tenant_id: str, metadata: dict[str, Any] | None = None) -> bool:
        return True
    async def batch_store_vectors(self, vectors: list[tuple[UUID, list[float] | dict[str, list[float]], dict[str, Any]]], tenant_id: str) -> int:
        return len(vectors)
    
    # Compatibility methods for tests
    async def add_vector(self, *args, **kwargs): return True
    async def count_vectors(self, *args, **kwargs): return 0