"""Qdrant vector store adapter for RAE-core.

Implements IVectorStore interface using Qdrant for similarity search.
"""

from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams
except ImportError:
    QdrantClient = None

from ..interfaces.vector import IVectorStore


class QdrantVectorStore(IVectorStore):
    """Qdrant implementation of IVectorStore.
    
    Requires qdrant-client package and access to Qdrant server.
    
    Collection schema:
    - Vectors: embeddings (dimension configurable, default 1536 for OpenAI)
    - Payload: {
        memory_id: UUID,
        tenant_id: str,
        agent_id: str,
        layer: str,
        content: str (optional, for debugging),
        importance: float,
        created_at: timestamp
      }
    """

    def __init__(
        self,
        collection_name: str = "rae_memories",
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        client: Optional["QdrantClient"] = None,
        embedding_dim: int = 1536,
        distance: str = "Cosine",
    ):
        """Initialize Qdrant vector store.
        
        Args:
            collection_name: Name of Qdrant collection
            url: Qdrant server URL (e.g., http://localhost:6333)
            api_key: Optional API key for Qdrant Cloud
            client: Existing QdrantClient instance
            embedding_dim: Dimension of embeddings (default: 1536 for OpenAI)
            distance: Distance metric (Cosine, Euclid, Dot)
        """
        if QdrantClient is None:
            raise ImportError(
                "qdrant-client is required for QdrantVectorStore. "
                "Install with: pip install qdrant-client"
            )

        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        
        # Distance metric mapping
        distance_map = {
            "Cosine": Distance.COSINE,
            "Euclid": Distance.EUCLID,
            "Dot": Distance.DOT,
        }
        self.distance = distance_map.get(distance, Distance.COSINE)

        if client:
            self.client = client
        elif url:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            # Use in-memory mode for testing
            self.client = QdrantClient(":memory:")

        self._initialized = False

    async def _ensure_collection(self):
        """Ensure collection exists with proper schema."""
        if self._initialized:
            return

        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=self.distance,
                ),
            )

        self._initialized = True

    async def add_vector(
        self,
        memory_id: UUID,
        embedding: List[float],
        tenant_id: str,
        agent_id: str,
        layer: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add a vector to Qdrant."""
        await self._ensure_collection()

        metadata = metadata or {}
        
        payload = {
            "memory_id": str(memory_id),
            "tenant_id": tenant_id,
            "agent_id": agent_id,
            "layer": layer,
            **metadata,
        }

        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=str(memory_id),
                        vector=embedding,
                        payload=payload,
                    )
                ],
            )
            return True
        except Exception:
            return False

    async def store_vector(
        self,
        memory_id: UUID,
        embedding: List[float],
        tenant_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Store a vector embedding."""
        metadata = metadata or {}
        agent_id = str(metadata.get("agent_id", "default"))
        layer = str(metadata.get("layer", "episodic"))
        return await self.add_vector(memory_id, embedding, tenant_id, agent_id, layer, metadata)

    async def update_vector(
        self,
        memory_id: UUID,
        embedding: List[float],
        tenant_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update a vector embedding."""
        return await self.store_vector(memory_id, embedding, tenant_id, metadata)

    async def batch_store_vectors(
        self,
        vectors: List[Tuple[UUID, List[float], Dict[str, Any]]],
        tenant_id: str,
    ) -> int:
        """Store multiple vectors in a batch."""
        await self._ensure_collection()
        
        points = []
        for memory_id, embedding, metadata in vectors:
            meta = metadata or {}
            agent_id = str(meta.get("agent_id", "default"))
            layer = str(meta.get("layer", "episodic"))
            
            payload = {
                "memory_id": str(memory_id),
                "tenant_id": tenant_id,
                "agent_id": agent_id,
                "layer": layer,
                **meta
            }
            
            points.append(PointStruct(
                id=str(memory_id),
                vector=embedding,
                payload=payload
            ))
            
        if not points:
            return 0

        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return len(points)
        except Exception:
            return 0

    async def search_similar(
        self,
        query_embedding: List[float],
        tenant_id: str,
        layer: Optional[str] = None,
        limit: int = 10,
        score_threshold: Optional[float] = None,
    ) -> List[Tuple[UUID, float]]:
        """Search for similar vectors using cosine similarity."""
        await self._ensure_collection()

        # Build filter
        must_conditions = [
            {"key": "tenant_id", "match": {"value": tenant_id}}
        ]
        
        if layer:
            must_conditions.append(
                {"key": "layer", "match": {"value": layer}}
            )

        query_filter = {"must": must_conditions} if must_conditions else None

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=query_filter,
                limit=limit,
                score_threshold=score_threshold,
            )

            return [
                (UUID(result.payload["memory_id"]), result.score)
                for result in results
            ]
        except Exception:
            return []

    async def get_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> Optional[List[float]]:
        """Get vector by memory ID."""
        await self._ensure_collection()

        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[str(memory_id)],
            )
            
            if result and len(result) > 0:
                # Verify tenant_id matches
                if result[0].payload.get("tenant_id") == tenant_id:
                    return result[0].vector
        except Exception:
            pass

        return None

    async def delete_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a vector."""
        await self._ensure_collection()

        try:
            # First verify it belongs to tenant
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[str(memory_id)],
            )
            
            if not result or result[0].payload.get("tenant_id") != tenant_id:
                return False

            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[str(memory_id)],
            )
            return True
        except Exception:
            return False

    async def delete_by_layer(
        self,
        tenant_id: str,
        agent_id: str,
        layer: str,
    ) -> int:
        """Delete all vectors in a layer."""
        await self._ensure_collection()

        try:
            # Use filter to delete
            delete_filter = {
                "must": [
                    {"key": "tenant_id", "match": {"value": tenant_id}},
                    {"key": "agent_id", "match": {"value": agent_id}},
                    {"key": "layer", "match": {"value": layer}},
                ]
            }

            result = self.client.delete(
                collection_name=self.collection_name,
                points_selector=delete_filter,
            )
            
            # Qdrant doesn't return count easily, return success indicator
            return 1 if result else 0
        except Exception:
            return 0

    async def count_vectors(
        self,
        tenant_id: str,
        layer: Optional[str] = None,
    ) -> int:
        """Count vectors matching criteria."""
        await self._ensure_collection()

        try:
            count_filter = {
                "must": [
                    {"key": "tenant_id", "match": {"value": tenant_id}}
                ]
            }
            
            if layer:
                count_filter["must"].append(
                    {"key": "layer", "match": {"value": layer}}
                )

            result = self.client.count(
                collection_name=self.collection_name,
                count_filter=count_filter,
            )
            
            return result.count if result else 0
        except Exception:
            return 0

    def close(self):
        """Close Qdrant client."""
        if hasattr(self.client, "close"):
            self.client.close()
