"""Main RAE Engine - Orchestrates all RAE-core components."""

from typing import Any, Dict, List, Optional
from uuid import UUID

from rae_core.config import RAESettings
from rae_core.interfaces.cache import ICacheProvider
from rae_core.interfaces.embedding import IEmbeddingProvider
from rae_core.interfaces.llm import ILLMProvider
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.interfaces.sync import ISyncProvider
from rae_core.interfaces.vector import IVectorStore
from rae_core.llm.orchestrator import LLMOrchestrator
from rae_core.reflection.engine import ReflectionEngine
from rae_core.search.engine import HybridSearchEngine
from rae_core.sync.protocol import SyncProtocol


class RAEEngine:
    """Main RAE Engine coordinating all components.

    Provides a unified interface for:
    - Memory storage and retrieval
    - Hybrid search (dense + sparse)
    - LLM orchestration
    - Reflection and meta-cognition
    - Memory synchronization
    """

    def __init__(
        self,
        memory_storage: IMemoryStorage,
        vector_store: IVectorStore,
        embedding_provider: IEmbeddingProvider,
        settings: Optional[RAESettings] = None,
        llm_provider: Optional[ILLMProvider] = None,
        cache_provider: Optional[ICacheProvider] = None,
        sync_provider: Optional[ISyncProvider] = None,
    ):
        """Initialize RAE Engine.

        Args:
            memory_storage: Memory storage provider
            vector_store: Vector database provider
            embedding_provider: Embedding provider
            settings: Optional RAE settings (creates default if not provided)
            llm_provider: Optional LLM provider
            cache_provider: Optional cache provider
            sync_provider: Optional sync provider
        """
        self.memory_storage = memory_storage
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider
        self.settings = settings or RAESettings()
        self.llm_provider = llm_provider
        self.cache_provider = cache_provider
        self.sync_provider = sync_provider

        # Initialize sub-engines
        self.search_engine = HybridSearchEngine(
            vector_store=vector_store,
            embedding_provider=embedding_provider,
            cache_provider=cache_provider,
        )

        self.reflection_engine = ReflectionEngine(
            memory_storage=memory_storage,
            llm_provider=llm_provider,
        )

        # Initialize LLM orchestrator if LLM provider is available
        self.llm_orchestrator: Optional[LLMOrchestrator] = None
        if llm_provider:
            from rae_core.llm.config import LLMConfig

            llm_config = LLMConfig(
                default_provider="default",
                providers={},
                enable_cache=self.settings.cache_enabled,
                cache_ttl=self.settings.cache_ttl,
            )
            self.llm_orchestrator = LLMOrchestrator(
                config=llm_config,
                providers={"default": llm_provider},
                cache=cache_provider,
            )

        # Initialize sync protocol if sync provider is available
        self.sync_protocol: Optional[SyncProtocol] = None
        if sync_provider and self.settings.sync_enabled:
            self.sync_protocol = SyncProtocol(
                sync_provider=sync_provider,
                encryption_enabled=self.settings.sync_encryption_enabled,
            )

    # Memory operations

    async def store_memory(
        self,
        tenant_id: str,
        agent_id: str,
        content: str,
        memory_type: str = "sensory",
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UUID:
        """Store a new memory.

        Args:
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            content: Memory content
            memory_type: Type of memory (sensory, working, episodic, semantic)
            importance: Importance score (0-1)
            tags: Optional tags
            metadata: Optional metadata

        Returns:
            Memory ID
        """
        return await self.memory_storage.store_memory(
            tenant_id=tenant_id,
            agent_id=agent_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {},
        )

    async def retrieve_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a memory by ID.

        Args:
            memory_id: Memory identifier
            tenant_id: Tenant identifier

        Returns:
            Memory record or None if not found
        """
        return await self.memory_storage.get_memory(
            memory_id=memory_id,
            tenant_id=tenant_id,
        )

    async def search_memories(
        self,
        query: str,
        tenant_id: str,
        agent_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
        use_reranker: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search memories using hybrid search.

        Args:
            query: Search query
            tenant_id: Tenant identifier
            agent_id: Optional agent filter
            memory_type: Optional memory type filter
            top_k: Number of results (uses settings default if not specified)
            similarity_threshold: Similarity threshold (uses settings default if not specified)
            use_reranker: Whether to use reranking

        Returns:
            List of matching memories
        """
        search_config = self.settings.get_search_config()
        top_k = top_k or search_config["top_k"]
        similarity_threshold = similarity_threshold or search_config["similarity_threshold"]

        filters = {}
        if agent_id:
            filters["agent_id"] = agent_id
        if memory_type:
            filters["memory_type"] = memory_type

        results = await self.search_engine.search(
            query=query,
            tenant_id=tenant_id,
            filters=filters,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
        )

        if use_reranker and len(results) > 0:
            rerank_top_k = search_config["rerank_top_k"]
            results = await self.search_engine.rerank(
                query=query,
                results=results[:rerank_top_k],
            )

        return results

    # Reflection operations

    async def run_reflection_cycle(
        self,
        tenant_id: str,
        agent_id: str,
        trigger_type: str = "scheduled",
    ) -> Dict[str, Any]:
        """Run a reflection cycle.

        Args:
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            trigger_type: Type of trigger

        Returns:
            Cycle execution summary
        """
        return await self.reflection_engine.run_reflection_cycle(
            tenant_id=tenant_id,
            agent_id=agent_id,
            trigger_type=trigger_type,
        )

    async def generate_reflection(
        self,
        memory_ids: List[UUID],
        tenant_id: str,
        agent_id: str,
        reflection_type: str = "consolidation",
    ) -> Dict[str, Any]:
        """Generate a reflection from specific memories.

        Args:
            memory_ids: List of memory IDs
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            reflection_type: Type of reflection

        Returns:
            Reflection result
        """
        return await self.reflection_engine.generate_reflection(
            memory_ids=memory_ids,
            tenant_id=tenant_id,
            agent_id=agent_id,
            reflection_type=reflection_type,
        )

    # Sync operations

    async def sync_memories(
        self,
        tenant_id: str,
        agent_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Synchronize memories with remote.

        Args:
            tenant_id: Tenant identifier
            agent_id: Agent identifier

        Returns:
            Sync result or None if sync is not enabled
        """
        if not self.sync_protocol:
            return None

        response = await self.sync_protocol.sync(
            tenant_id=tenant_id,
            agent_id=agent_id,
        )

        return {
            "success": response.success,
            "synced_count": len(response.synced_memory_ids),
            "conflicts": len(response.conflicts),
            "error": response.error_message,
        }

    # LLM operations

    async def generate_text(
        self,
        prompt: str,
        provider_name: Optional[str] = None,
        **kwargs,
    ) -> Optional[str]:
        """Generate text using LLM.

        Args:
            prompt: Prompt text
            provider_name: Optional provider name
            **kwargs: Additional arguments

        Returns:
            Generated text or None if LLM is not available
        """
        if not self.llm_orchestrator:
            return None

        # Use settings defaults
        llm_config = self.settings.get_llm_config()
        kwargs.setdefault("temperature", llm_config["temperature"])
        kwargs.setdefault("max_tokens", llm_config["max_tokens"])

        response, _ = await self.llm_orchestrator.generate(
            prompt=prompt,
            provider_name=provider_name,
            **kwargs,
        )

        return response

    # Health and status

    def get_status(self) -> Dict[str, Any]:
        """Get engine status.

        Returns:
            Status information
        """
        return {
            "settings": {
                "sensory_max_size": self.settings.sensory_max_size,
                "working_max_size": self.settings.working_max_size,
                "episodic_max_size": self.settings.episodic_max_size,
                "semantic_max_size": self.settings.semantic_max_size,
                "decay_rate": self.settings.decay_rate,
                "vector_backend": self.settings.vector_backend,
            },
            "features": {
                "llm_enabled": self.llm_orchestrator is not None,
                "cache_enabled": self.settings.cache_enabled,
                "sync_enabled": self.sync_protocol is not None,
                "otel_enabled": self.settings.otel_enabled,
            },
            "version": "0.4.0",
        }
