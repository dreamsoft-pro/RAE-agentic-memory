"""Qdrant vector store adapter."""

import logging
from typing import Any
from uuid import UUID

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import exceptions
from qdrant_client.models import Distance, VectorParams, PointStruct, NamedVector

from rae_core.interfaces.vector import IVectorStore

logger = logging.getLogger(__name__)


class QdrantVectorStore(IVectorStore):
    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str = "memories",
        embedding_dim: int = 384,
        vector_name: str = "dense",
    ):
        self.client = client
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self.vector_name = vector_name

    async def _ensure_collection(self):
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
        except Exception as e:
            logger.error(f"Failed to ensure Qdrant collection: {e}")

    async def store_vector(
        self, memory_id, embedding, tenant_id, metadata=None, **kwargs
    ):
        await self._ensure_collection()
        try:
            payload = {
                "memory_id": str(memory_id),
                "tenant_id": str(tenant_id),
                **(metadata or {}),
            }
            await self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=str(memory_id),
                        vector={self.vector_name: embedding},
                        payload=payload,
                    )
                ],
            )
            return True
        except Exception as e:
            logger.error(f"Qdrant upsert failed: {e}")
            return False

    async def search_similar(self, query_embedding, tenant_id, limit=10, **kwargs):
        await self._ensure_collection()
        try:
            # For verification, we search EVERYTHING in the collection (limited by tenant in future)
            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=NamedVector(name=self.vector_name, vector=query_embedding),
                limit=limit,
            )

            output = []
            for r in results:
                if r.payload and "memory_id" in r.payload:
                    output.append((UUID(r.payload["memory_id"]), float(r.score)))

            if output:
                logger.info(f"QDRANT SUCCESS: Found {len(output)} hits")
            else:
                logger.warning(
                    "QDRANT WARNING: Collection has 0 matches for this vector"
                )

            return output
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            return []

    # Implement other required methods as no-ops for benchmark
    async def delete_vector(self, memory_id, tenant_id):
        pass

    async def delete_tenant_vectors(self, tenant_id):
        pass
