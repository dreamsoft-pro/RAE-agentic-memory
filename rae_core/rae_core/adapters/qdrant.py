"""
Qdrant adapter for vector storage.

Implements vector search operations using Qdrant.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class QdrantVectorAdapter:
    """
    Qdrant adapter for vector operations.

    Handles embedding storage and similarity search.
    """

    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str = "memories",
        vector_size: int = 1536,
    ):
        """
        Initialize adapter with Qdrant client.

        Args:
            client: Qdrant async client
            collection_name: Name of the collection
            vector_size: Dimension of embeddings (default: 1536 for OpenAI)
        """
        self.client = client
        self.collection_name = collection_name
        self.vector_size = vector_size

    async def ensure_collection(self):
        """Create collection if it doesn't exist."""
        collections = await self.client.get_collections()
        exists = any(
            c.name == self.collection_name for c in collections.collections
        )

        if not exists:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    async def upsert_vector(
        self,
        memory_id: str,
        embedding: List[float],
        metadata: Dict[str, Any],
    ) -> str:
        """
        Upsert memory embedding into Qdrant.

        Args:
            memory_id: Memory identifier
            embedding: Vector embedding
            metadata: Additional metadata (tenant_id, project, etc.)

        Returns:
            Point ID
        """
        await self.ensure_collection()

        point = PointStruct(
            id=memory_id,
            vector=embedding,
            payload=metadata,
        )

        await self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

        return memory_id

    async def search_similar(
        self,
        query_embedding: List[float],
        tenant_id: str,
        project: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.

        Args:
            query_embedding: Query vector
            tenant_id: Tenant filter
            project: Project filter
            limit: Number of results
            filters: Additional filters

        Returns:
            List of search results with scores
        """
        # Build Qdrant filter
        must_conditions = [
            {"key": "tenant_id", "match": {"value": tenant_id}},
            {"key": "project", "match": {"value": project}},
        ]

        if filters:
            if "layer" in filters:
                must_conditions.append(
                    {"key": "layer", "match": {"value": filters["layer"]}}
                )

            if "min_importance" in filters:
                must_conditions.append(
                    {
                        "key": "importance",
                        "range": {"gte": filters["min_importance"]},
                    }
                )

        search_results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter={"must": must_conditions} if must_conditions else None,
            limit=limit,
        )

        results = []
        for hit in search_results:
            results.append(
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload,
                }
            )

        return results

    async def delete_vector(self, memory_id: str) -> bool:
        """Delete vector by memory ID."""
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=[memory_id],
            )
            return True
        except Exception:
            return False

    async def get_vector(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve vector by ID."""
        try:
            points = await self.client.retrieve(
                collection_name=self.collection_name,
                ids=[memory_id],
                with_vectors=True,
            )

            if not points:
                return None

            point = points[0]
            return {
                "id": point.id,
                "vector": point.vector,
                "payload": point.payload,
            }
        except Exception:
            return None

    async def count_vectors(
        self, tenant_id: str, project: str
    ) -> int:
        """Count vectors for tenant and project."""
        must_conditions = [
            {"key": "tenant_id", "match": {"value": tenant_id}},
            {"key": "project", "match": {"value": project}},
        ]

        result = await self.client.count(
            collection_name=self.collection_name,
            count_filter={"must": must_conditions},
        )

        return result.count
