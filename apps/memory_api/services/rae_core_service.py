import asyncio
import json
import logging
import os
from typing import Any, Optional, cast
from uuid import UUID, uuid4

import structlog
from qdrant_client import AsyncQdrantClient

from apps.memory_api.services.dashboard_websocket import DashboardWebSocketService
from apps.memory_api.services.embedding import (
    LocalEmbeddingProvider,
)
from apps.memory_api.services.llm import get_llm_provider
from apps.memory_api.services.token_savings_service import TokenSavingsService
from rae_adapters.postgres import PostgreSQLStorage
from rae_adapters.qdrant import QdrantVectorStore
from rae_adapters.redis import RedisCache
from rae_core.config import RAESettings
from rae_core.embedding.manager import EmbeddingManager
from rae_core.engine import RAEEngine
from rae_core.exceptions.base import (
    ContractViolationError,
    SecurityPolicyViolationError,
)
from rae_core.interfaces.cache import ICacheProvider
from rae_core.interfaces.database import IDatabaseProvider
from rae_core.interfaces.reranking import IReranker
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.interfaces.vector import IVectorStore
from rae_core.models.interaction import AgentAction, RAEInput
from rae_core.models.search import SearchResponse
from rae_core.runtime import RAERuntime
from rae_core.types.enums import InformationClass, MemoryLayer

logger = structlog.get_logger(__name__)


class RAECoreService:
    """
    Integration service for RAE-Core.
    """

    def __init__(self, settings: RAESettings, qdrant_client: Any = None, postgres_pool: Any = None) -> None:
        self.settings = settings
        self.qdrant_client = qdrant_client
        self.postgres_pool = postgres_pool
        self.szubar_mode = False
        
        # Initialize basic manager
        self.embedding_provider = EmbeddingManager(
            default_provider=LocalEmbeddingProvider()
        )

    async def ainit(self) -> None:
        """Asynchronous initialization of components."""
        settings = self.settings
        
        # 1. Initialize Adapters
        ignore_db = settings.RAE_DB_MODE == "ignore"
        self.cache_adapter = RedisCache(url=settings.REDIS_URL)

        if self.postgres_pool and not ignore_db:
            self.postgres_adapter = PostgreSQLStorage(pool=self.postgres_pool)
        else:
            from rae_adapters.memory import InMemoryStorage
            self.postgres_adapter = cast(IMemoryStorage, InMemoryStorage())

        if self.qdrant_client and not ignore_db:
            dim = self.embedding_provider.get_dimension()
            v_name = "nomic" if dim == 768 else "dense"
            self.qdrant_adapter = QdrantVectorStore(
                client=cast(Any, self.qdrant_client),
                embedding_dim=dim,
                distance=getattr(settings, "RAE_VECTOR_DISTANCE", "Cosine"),
                vector_name=v_name,
            )
        else:
            from rae_adapters.memory import InMemoryVectorStore
            self.qdrant_adapter = InMemoryVectorStore()

        # 2. Initalize Embedding Provider
        if settings.RAE_EMBEDDING_BACKEND == "onnx":
            self._register_onnx_provider(settings)

        # 3. Initialize Engine
        self.engine = RAEEngine(
            memory_storage=self.postgres_adapter,
            vector_store=self.qdrant_adapter,
            embedding_provider=self.embedding_provider,
            cache_provider=self.cache_adapter,
        )

        # 4. Initialize Reflection
        from apps.memory_api.services.reflection_engine_v2 import ReflectionEngineV2
        from rae_core.reflection.layers.coordinator import ReflectionCoordinator

        self.reflection_engine = ReflectionEngineV2(self)
        self.reflection_coordinator = ReflectionCoordinator(
            mode=settings.RAE_PROFILE if settings.RAE_PROFILE in ["standard", "advanced"] else "standard",
            enforce_hard_frames=True,
            storage=self.postgres_adapter,
            llm_provider=get_llm_provider(settings),
            llm_model=settings.RAE_LLM_MODEL_DEFAULT,
            strategy=settings.RAE_REFLECTION_STRATEGY
        )

        self.runtime = RAERuntime(cast(Any, self.engine), None)

    def _register_onnx_provider(self, settings: RAESettings) -> None:
        try:
            from rae_core.embedding.native import NativeEmbeddingProvider
            model_path = settings.ONNX_EMBEDDER_PATH or "models/nomic-embed-text-v1.5/model.onnx"
            if not os.path.exists(model_path): model_path = "models/all-MiniLM-L6-v2/model.onnx"
            if os.path.exists(model_path):
                tokenizer_path = os.path.join(os.path.dirname(model_path), "tokenizer.json")
                model_name = "nomic" if "nomic" in model_path.lower() else "mini-lm"
                onnx_provider = NativeEmbeddingProvider(
                    model_path=model_path, tokenizer_path=tokenizer_path, model_name=model_name, use_gpu=settings.RAE_USE_GPU
                )
                self.embedding_provider.register_provider(model_name, onnx_provider)
                self.embedding_provider._default_provider = onnx_provider
                self.embedding_provider.default_model_name = model_name
        except Exception as e:
            logger.warning("failed_to_register_onnx", error=str(e))

    async def store_memory(
        self,
        tenant_id: str,
        project: Optional[str],
        content: str,
        source: str,
        importance: Optional[float] = None,
        tags: Optional[list] = None,
        layer: Optional[str] = None,
        session_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        ttl: Optional[int] = None,
        info_class: str = "internal",
        metadata: Optional[dict] = None,
        governance: Optional[dict] = None,
        human_label: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> str:
        target_layer = layer or MemoryLayer.EPISODIC
        self._enforce_security_policy(info_class, target_layer)

        project_canonical = project or "default"
        agent_canonical = agent_id or "default"
        metadata = metadata or {}
        tags = tags or []

        # Background Audit
        if "agent_decision" in tags or layer == "working":
            async def run_async_audit():
                try:
                    payload = {"analysis": content}
                    sources = await self.engine.search_memories(query=content, tenant_id=tenant_id, top_k=3)
                    payload.update({
                        "retrieved_sources": [str(m["id"]) for m in sources],
                        "retrieved_sources_content": [m["content"] for m in sources],
                        "decision": metadata.get("decision", "proceed"),
                        "confidence": metadata.get("confidence", 0.5),
                        "metadata": {**metadata, "project": project_canonical}
                    })
                    
                    validation = await self.reflection_coordinator.run_and_store_reflections(
                        payload, tenant_id=tenant_id, agent_id="oracle_auditor",
                        store_callback=self.engine.store_memory
                    )
                    
                    audit_name = human_label or f"Audit: {project_canonical}"
                    await self.engine.store_memory(
                        tenant_id=tenant_id, agent_id="oracle_auditor",
                        content=f"AUDIT {audit_name}: {validation['final_decision']}",
                        layer="reflective", tags=["audit_log"],
                        metadata={"validation": validation}
                    )
                except Exception as e:
                    logger.warning("background_audit_failed", error=str(e))

            asyncio.create_task(run_async_audit())

        return await self.engine.store_memory(
            tenant_id=tenant_id, project=project_canonical, content=content, source=source,
            importance=importance, tags=tags, layer=target_layer, session_id=session_id,
            memory_type=memory_type, ttl=ttl, metadata=metadata, agent_id=agent_canonical
        )

    def _enforce_security_policy(self, info_class: str, layer: str) -> None:
        if info_class == "restricted" and layer != "working":
            raise SecurityPolicyViolationError("Restricted data can only be stored in the working layer")

    async def query_memories(self, tenant_id: str, project: str, query: str, k: int = 10, layers: Optional[list[str]] = None, filters: Optional[dict] = None) -> SearchResponse:
        return await self.engine.search_memories(query=query, tenant_id=tenant_id, top_k=k, layers=layers, filters=filters)

    async def list_memories(self, tenant_id: str, limit: int = 50, offset: int = 0, project: Optional[str] = None, layer: Optional[str] = None) -> list[dict]:
        return await self.engine.memory_storage.list_memories(tenant_id=tenant_id, limit=limit, offset=offset, project=project, layer=layer)

    async def get_memory(self, memory_id: str, tenant_id: str) -> Optional[dict]:
        return await self.engine.get_memory(memory_id, tenant_id)

    async def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        return await self.engine.delete_memory(memory_id, tenant_id)

    async def get_statistics(self, tenant_id: str, project: str) -> dict:
        return await self.engine.get_statistics(tenant_id, project)

    async def update_memory_access_batch(self, memory_ids: list[str], tenant_id: str) -> bool:
        return await self.engine.update_memory_access_batch(memory_ids, tenant_id)
