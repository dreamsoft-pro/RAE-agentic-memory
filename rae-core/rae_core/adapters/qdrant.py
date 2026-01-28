"""Qdrant vector store adapter."""

import math
from typing import Any, cast
from uuid import UUID

import structlog
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    NamedVector,
    PointStruct,
    VectorParams,
)

from rae_core.interfaces.vector import IVectorStore

logger = structlog.get_logger(__name__)


class QdrantVectorStore(IVectorStore):
    """Qdrant implementation of the Vector Store interface."""

    def __init__(
        self,
        client: AsyncQdrantClient | None = None,
        url: str | None = None,
        api_key: str | None = None,
        collection_name: str = "memories",
        embedding_dim: int = 384,
        vector_name: str = "dense",
    ):
        """Initialize Qdrant Vector Store.

        Args:
            client: Existing Qdrant client instance.
            url: Qdrant URL (if client is not provided).
            api_key: Qdrant API Key (if client is not provided).
            collection_name: Name of the collection.
            embedding_dim: Dimension of embeddings (default 384).
            vector_name: Name of the named vector (default "dense").
        """
        if client:
            self.client = client
        else:
            if not url:
                url = "http://localhost:6333"  # Default fallback
            self.client = AsyncQdrantClient(url=url, api_key=api_key)

        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self.vector_name = vector_name
        self._initialized = False

    async def _ensure_collection(self) -> None:
        """Ensure the collection exists with the correct schema."""
        if self._initialized:
            return

        try:
            collections = await self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            if self.collection_name not in collection_names:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config={
                        self.vector_name: VectorParams(
                            size=self.embedding_dim, distance=Distance.COSINE
                        )
                    },
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to ensure Qdrant collection: {e}")
            # Do not set initialized to True if failed, so we retry

    def _build_filter(
        self,
        tenant_id: str,
        layer: str | None = None,
        agent_id: str | None = None,
        session_id: str | None = None,
        project: str | None = None,
        extra_filters: dict[str, Any] | None = None,
    ) -> Filter:
        """Build Qdrant Filter from RAE metadata."""
        must_conditions = [
            FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))
        ]

        if layer:
            must_conditions.append(
                FieldCondition(key="layer", match=MatchValue(value=layer))
            )
        if agent_id:
            must_conditions.append(
                FieldCondition(key="agent_id", match=MatchValue(value=agent_id))
            )
        if session_id:
            must_conditions.append(
                FieldCondition(key="session_id", match=MatchValue(value=session_id))
            )
        if project:
            must_conditions.append(
                FieldCondition(key="project", match=MatchValue(value=project))
            )

        if extra_filters:
            for key, value in extra_filters.items():
                # Basic support for exact match
                must_conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )

        return Filter(must=must_conditions)

    async def store_vector(
        self,
        memory_id: UUID,
        embedding: list[float] | dict[str, list[float]],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Store a single vector."""
        return (
            await self.batch_store_vectors(
                [(memory_id, embedding, metadata or {})], tenant_id
            )
            == 1
        )

    async def batch_store_vectors(
        self,
        vectors: list[
            tuple[UUID, list[float] | dict[str, list[float]], dict[str, Any]]
        ],
        tenant_id: str,
    ) -> int:
        """Store multiple vectors in a batch."""
        if not vectors:
            return 0

        await self._ensure_collection()
        points = []

        for mem_id, emb, meta in vectors:
            # Handle named vectors vs list
            if isinstance(emb, dict):
                vector_data = emb  # It's already a dictionary of named vectors
            else:
                vector_data = {self.vector_name: emb}

            # Prepare payload
            payload = {
                "memory_id": str(mem_id),
                "tenant_id": str(tenant_id),
                **(meta or {}),
            }

            points.append(
                PointStruct(id=str(mem_id), vector=vector_data, payload=payload)
            )

        try:
            await self.client.upsert(
                collection_name=self.collection_name, points=points
            )
            return len(points)
        except Exception as e:
            logger.error(f"Qdrant batch upsert failed: {e}")
            return 0

    async def get_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> list[float] | None:
        """Retrieve a vector embedding by ID."""
        await self._ensure_collection()
        try:
            results = await self.client.retrieve(
                collection_name=self.collection_name,
                ids=[str(memory_id)],
                with_vectors=True,
                with_payload=True,
            )

            if not results:
                return None

            record = results[0]
            # Security check: Ensure tenant matches
            if not record.payload or record.payload.get("tenant_id") != tenant_id:
                return None

            if record.vector:
                if isinstance(record.vector, dict):
                    return cast(list[float] | None, record.vector.get(self.vector_name))
                return cast(list[float] | None, record.vector)

            return None
        except Exception as e:
            logger.error(f"Qdrant get_vector failed: {e}")
            return None

    async def update_vector(
        self,
        memory_id: UUID,
        embedding: list[float] | dict[str, list[float]],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Update a vector embedding."""
        return await self.store_vector(memory_id, embedding, tenant_id, metadata)

    async def delete_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a vector."""
        await self._ensure_collection()
        try:
            # First check if it belongs to tenant
            existing = await self.client.retrieve(
                collection_name=self.collection_name,
                ids=[str(memory_id)],
                with_payload=True,
            )
            if (
                not existing
                or not existing[0].payload
                or existing[0].payload.get("tenant_id") != tenant_id
            ):
                return False

            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=[str(memory_id)]),
            )
            return True
        except Exception as e:
            logger.error(f"Qdrant delete failed: {e}")
            return False

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
        project: str | None = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float]]:
        """Search for similar vectors."""
        await self._ensure_collection()

        search_filter = self._build_filter(
            tenant_id=tenant_id,
            layer=layer,
            agent_id=agent_id,
            session_id=session_id,
            project=project,
            extra_filters=filters,
        )

        try:
            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=NamedVector(name=self.vector_name, vector=query_embedding),
                query_filter=search_filter,
                limit=limit,
                score_threshold=score_threshold,
            )

            output = []
            for r in results:
                if r.payload and "memory_id" in r.payload:
                    output.append((UUID(r.payload["memory_id"]), float(r.score)))

            return output
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            return []

    # --- Extra Methods Required by Tests / Legacy Support ---

    async def add_vector(
        self,
        memory_id: UUID,
        embedding: list[float],
        tenant_id: str,
        agent_id: str | None = None,
        layer: str | None = None,
    ) -> bool:
        """Alias for store_vector (Legacy)."""
        metadata = {}
        if agent_id:
            metadata["agent_id"] = agent_id
        if layer:
            metadata["layer"] = layer
        return await self.store_vector(memory_id, embedding, tenant_id, metadata)

    async def count_vectors(self, tenant_id: str, layer: str | None = None) -> int:
        """Count vectors for a tenant."""
        await self._ensure_collection()
        try:
            count_filter = self._build_filter(tenant_id=tenant_id, layer=layer)
            result = await self.client.count(
                collection_name=self.collection_name, count_filter=count_filter
            )
            return result.count
        except Exception as e:
            logger.error(f"Qdrant count failed: {e}")
            return 0

    async def delete_by_layer(self, tenant_id: str, agent_id: str, layer: str) -> int:
        """Delete vectors matching criteria."""
        await self._ensure_collection()
        try:
            del_filter = self._build_filter(
                tenant_id=tenant_id, agent_id=agent_id, layer=layer
            )
            # Qdrant python client delete_by_filter returns UpdateResult?
            _result = await self.client.delete(
                collection_name=self.collection_name, points_selector=del_filter
            )
            # Cannot easily get count of deleted items without extra query
            return 1  # Assume success
        except Exception as e:
            logger.error(f"Qdrant delete_by_layer failed: {e}")
            return 0

    async def search_with_contradiction_penalty(
        self,
        query_embedding: list[float],
        tenant_id: str,
        penalty_factor: float = 0.5,
        limit: int = 10,
    ) -> list[tuple[UUID, float]]:
        """Experimental: Search and penalize results that contradict the query."""
        # 1. Standard search
        results = await self.search_similar(query_embedding, tenant_id, limit=limit)
        if not results:
            return []

        final_results = []
        for m_id, score in results:
            # 2. Fetch the vector
            vec = await self.get_vector(m_id, tenant_id)
            if not vec:
                final_results.append((m_id, score))
                continue

            # 3. Calculate contradiction (Cosine Similarity)
            # High cosine = similar, Low/Negative = contradictory
            similarity = self._cosine_similarity(query_embedding, vec)

            # If vectors are contradictory (e.g. angle > 90 deg, sim < 0), penalize
            if similarity < 0.15:  # Threshold from test
                score *= penalty_factor

            final_results.append((m_id, score))

        # Re-sort
        return sorted(final_results, key=lambda x: x[1], reverse=True)

    def _cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        """Calculate cosine similarity."""
        if len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(b * b for b in v2))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)
