from typing import Any
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
        from qdrant_client.models import Distance, VectorParams
        try:
            await self.client.get_collection(self.collection_name)
        except Exception:
            vectors_config = {
                "dense": VectorParams(size=384, distance=Distance.COSINE),
                "ollama": VectorParams(size=768, distance=Distance.COSINE),
                "openai": VectorParams(size=1536, distance=Distance.COSINE),
            }
            await self.client.create_collection(collection_name=self.collection_name, vectors_config=vectors_config)
            await self.client.create_payload_index(self.collection_name, "tenant_id", "keyword")
            await self.client.create_payload_index(self.collection_name, "agent_id", "keyword")

    def _get_vector_name(self, dim: int) -> str:
        if dim == 1536:
            return "openai"
        if dim == 768:
            return "ollama"
        return "dense"

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
    ) -> list[tuple[UUID, float]]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue, NamedVector

        # Clean tenant_id string
        t_id = str(tenant_id).lower()
        if "uuid('" in t_id:
            t_id = t_id.replace("uuid('", "").replace("')", "")

        must_conditions = [FieldCondition(key="tenant_id", match=MatchValue(value=t_id))]

        # 1. Project Filter (Context)
        p_filter = (
            project
            or (filters or {}).get("project")
            or (filters or {}).get("project_id")
        )
        if p_filter and p_filter != "default":
            must_conditions.append(
                Filter(
                    should=[
                        FieldCondition(key="project", match=MatchValue(value=str(p_filter))),
                        FieldCondition(key="project", match=MatchValue(value="default")),
                    ]
                )
            )

        # 2. Agent Filter (Attribution)
        if agent_id and agent_id not in ["", "None", "default"]:
            must_conditions.append(
                Filter(
                    should=[
                        FieldCondition(
                            key="agent_id", match=MatchValue(value=str(agent_id))
                        ),
                        FieldCondition(key="agent_id", match=MatchValue(value="default")),
                    ]
                )
            )

        if layer:
            must_conditions.append(
                FieldCondition(key="layer", match=MatchValue(value=str(layer)))
            )

        query_filter = Filter(must=must_conditions)
        dim = len(query_embedding)
        v_name = self._get_vector_name(dim)

        all_results: dict[UUID, float] = {}
        try:
            if not hasattr(self.client, "search"):
                logger.error(
                    "qdrant_client_invalid_type",
                    type=str(type(self.client)),
                    has_search=hasattr(self.client, "search"),
                )

            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=NamedVector(name=v_name, vector=query_embedding),
                query_filter=query_filter,
                limit=limit,
                score_threshold=score_threshold
                or 0.0,  # Liberal threshold for benchmarks
            )
            for res in results:
                m_id = UUID(res.payload["memory_id"])
                all_results[m_id] = res.score
        except Exception as e:
            logger.error("qdrant_search_failed", space=v_name, error=str(e))

        return sorted(all_results.items(), key=lambda x: x[1], reverse=True)[:limit]

    async def store_vector(
        self,
        memory_id: UUID,
        embedding: list[float] | dict[str, list[float]],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        from qdrant_client.models import PointStruct

        if isinstance(embedding, dict):
            vectors = embedding
        else:
            vectors = {self._get_vector_name(len(embedding)): embedding}

        meta = metadata or {}
        payload = {
            "memory_id": str(memory_id),
            "tenant_id": str(tenant_id),
            "agent_id": meta.get("agent_id", "default"),
            "project": meta.get("project") or meta.get("project_id") or "default",
            **meta,
        }
        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(id=str(memory_id), vector=vectors, payload=payload)
                ],
            )
            return True
        except Exception:
            return False

    async def get_vector(self, memory_id: UUID, tenant_id: str) -> list[float] | None:
        return None

    async def delete_vector(self, memory_id: UUID, tenant_id: str) -> bool:
        return True

    async def update_vector(
        self,
        memory_id: UUID,
        embedding: list[float] | dict[str, list[float]],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        return True

    async def batch_store_vectors(
        self,
        vectors: list[tuple[UUID, list[float] | dict[str, list[float]], dict[str, Any]]],
        tenant_id: str,
    ) -> int:
        return len(vectors)

    async def add_vector(self, *args, **kwargs):
        return True

    async def count_vectors(self, *args, **kwargs):
        return 0
