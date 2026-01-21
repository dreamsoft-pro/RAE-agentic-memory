from typing import Any, Optional, List, Dict
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
        self._collection_info = None

    async def _ensure_collection(self):
        # In a real scenario, we would check if collection exists
        pass

    async def _get_compatible_vector_names(self, query_dim: int) -> List[str]:
        """Discover all vector spaces in the collection that match the query dimension."""
        try:
            collection_info = await self.client.get_collection(self.collection_name)
            vector_config = collection_info.config.params.vectors
            
            compatible_names = []
            # Handle both single vector and named vectors configurations
            if hasattr(vector_config, 'items'): # Named vectors dict
                for name, params in vector_config.items():
                    if params.size == query_dim:
                        compatible_names.append(name)
            elif hasattr(vector_config, 'size'): # Single vector
                if vector_config.size == query_dim:
                    compatible_names.append("") # Default unnamed vector
            
            if not compatible_names:
                # Fallback to defaults if discovery fails or collection is empty
                if query_dim == 1536: return ["openai"]
                return ["ollama", "dense"]
                
            return compatible_names
        except Exception as e:
            logger.warning("qdrant_discovery_failed", error=str(e))
            if query_dim == 1536: return ["openai"]
            return ["ollama", "dense"]

    async def search_similar(
        self,
        query_embedding: list[float],
        tenant_id: str,
        layer: str | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
        agent_id: str | None = None,
        session_id: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[tuple[UUID, float]]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        # Build filter
        must_conditions = [
            FieldCondition(key="tenant_id", match=MatchValue(value=str(tenant_id)))
        ]
        if agent_id:
            must_conditions.append(FieldCondition(key="agent_id", match=MatchValue(value=str(agent_id))))
        if layer:
            must_conditions.append(FieldCondition(key="layer", match=MatchValue(value=str(layer))))

        if filters:
            for key, value in filters.items():
                if key in ["tenant_id", "agent_id", "session_id", "layer", "score_threshold"]:
                    continue
                must_conditions.append(FieldCondition(key=key, match=MatchValue(value=str(value))))

        query_filter = Filter(must=must_conditions)
        query_dim = len(query_embedding)
        
        # DISCOVER: Find all spaces we can search in
        vector_names = await self._get_compatible_vector_names(query_dim)
        
        all_results = {}
        
        from qdrant_client.models import NamedVector
        
        for v_name in vector_names:
            try:
                # Prepare query (handle unnamed default vector if v_name is "")
                search_vector = query_embedding if not v_name else NamedVector(name=v_name, vector=query_embedding)
                
                results = await self.client.search(
                    collection_name=self.collection_name,
                    query_vector=search_vector,
                    query_filter=query_filter,
                    limit=limit,
                    score_threshold=score_threshold,
                )
                
                for res in results:
                    m_id = UUID(res.payload["memory_id"])
                    # Keep best score if found in multiple spaces
                    if m_id not in all_results or res.score > all_results[m_id]:
                        all_results[m_id] = res.score
                        
            except Exception as e:
                logger.error("qdrant_space_search_failed", space=v_name, error=str(e))

        # Sort merged results by score
        sorted_results = sorted(all_results.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:limit]

    async def store_memory(self, *args, **kwargs):
        pass