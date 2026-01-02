from typing import TYPE_CHECKING, Any, List, Optional, cast

import litellm

from apps.memory_api.metrics import embedding_time_histogram
from rae_core.interfaces.embedding import IEmbeddingProvider

try:  # pragma: no cover
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:  # pragma: no cover
    SentenceTransformer = None  # type: ignore[assignment,misc]
    SENTENCE_TRANSFORMERS_AVAILABLE = False

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer  # noqa: F401

# --- Embedding Model Loading ---
# This logic is moved from the old qdrant_client.py


class EmbeddingService:
    def __init__(self, settings: Optional[Any] = None):
        self._settings = settings
        self.model: Optional["SentenceTransformer"] = None
        self._initialized = False
        self.use_litellm = False
        self.litellm_model = "text-embedding-3-small"  # Default fallback

    @property
    def settings(self):
        from apps.memory_api.config import settings as default_settings

        return self._settings or default_settings

    def _ensure_available(self) -> None:
        """Check availability of local embedding models or fall back to LiteLLM."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self.use_litellm = True
            # Determine best default model based on env
            if self.settings.RAE_LLM_BACKEND == "ollama":
                self.litellm_model = "ollama/nomic-embed-text"
            elif self.settings.OPENAI_API_KEY:
                self.litellm_model = "text-embedding-3-small"

            print(
                f"SentenceTransformers not found. Falling back to LiteLLM with model: {self.litellm_model}"
            )

    def _initialize_model(self) -> None:
        """Lazy initialization of the embedding model."""
        if self._initialized:
            return

        self._ensure_available()

        if self.use_litellm:
            self._initialized = True
            return

        if self.settings.ONNX_EMBEDDER_PATH:
            # Placeholder for a real ONNX embedder class
            # A real implementation would load the model and tokenizer here.
            # self.model = self._get_onnx_embedder(self.settings.ONNX_EMBEDDER_PATH)
            print(
                f"Using ONNX embedder (placeholder) from: {self.settings.ONNX_EMBEDDER_PATH}"
            )
            # For now, we fall back to SentenceTransformer even if ONNX path is set,
            # as the ONNX implementation is just a placeholder.
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")  # type: ignore[misc]
        else:
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")  # type: ignore[misc]
            print("Using SentenceTransformer 'all-MiniLM-L6-v2'")

        self._initialized = True

    @embedding_time_histogram.time()
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates dense embeddings for a list of texts (synchronous).
        """
        self._initialize_model()

        if self.use_litellm:
            # Use LiteLLM for embeddings
            try:
                kwargs = {}
                if self.litellm_model.startswith("ollama/"):
                    kwargs["api_base"] = self.settings.OLLAMA_API_BASE or self.settings.OLLAMA_API_URL

                response = litellm.embedding(
                    model=self.litellm_model, input=texts, **kwargs
                )
                return [d["embedding"] for d in response["data"]]
            except Exception as e:
                print(f"LiteLLM embedding failed: {e}")
                # Fallback to dummy embeddings if API fails (to prevent crash in dev)
                # In prod this should probably raise
                return [[0.0] * 384 for _ in texts]

        embeddings = self.model.encode(texts)  # type: ignore[union-attr]
        return [emb.tolist() for emb in embeddings]

    async def generate_embeddings_async(self, texts: List[str]) -> List[List[float]]:
        """
        Generates dense embeddings for a list of texts (asynchronous).
        """
        # If remote ML service is configured and RAE_PROFILE is distributed, use it
        if self.settings.RAE_PROFILE == "distributed" or (
            self.settings.ML_SERVICE_URL
            and "localhost" not in self.settings.ML_SERVICE_URL
            and "127.0.0.1" not in self.settings.ML_SERVICE_URL
        ):
            from apps.memory_api.services.ml_service_client import MLServiceClient

            client = MLServiceClient(base_url=self.settings.ML_SERVICE_URL)
            try:
                result = await client.generate_embeddings(texts)
                return cast(List[List[float]], result.get("embeddings", []))
            finally:
                await client.close()

        # Initialize to check if we use litellm
        self._initialize_model()

        if self.use_litellm:
            # LiteLLM supports async via aembedding
            try:
                kwargs = {}
                if self.litellm_model.startswith("ollama/"):
                    kwargs["api_base"] = self.settings.OLLAMA_API_BASE or self.settings.OLLAMA_API_URL

                response = await litellm.aembedding(
                    model=self.litellm_model, input=texts, **kwargs
                )
                return [d["embedding"] for d in response["data"]]
            except Exception as e:
                print(f"LiteLLM async embedding failed: {e}")
                return [[0.0] * 384 for _ in texts]

        # Fallback to local execution (offloaded to thread pool if needed,
        # but here we just call the sync version for simplicity)
        import asyncio

        return await asyncio.to_thread(self.generate_embeddings, texts)

    async def generate_embeddings_for_model(
        self, texts: List[str], model_name: str
    ) -> List[List[float]]:
        """
        Generates embeddings for a specific model via LiteLLM.
        Useful for Multi-Vector Fusion where we need embeddings from multiple models.
        """
        try:
            kwargs = {}
            if model_name.startswith("ollama/"):
                kwargs["api_base"] = self.settings.OLLAMA_API_BASE or self.settings.OLLAMA_API_URL

            # Determine dimension for fallback
            dim = 384
            if "openai" in model_name or "text-embedding-3" in model_name:
                dim = 1536
            elif "nomic" in model_name:
                dim = 768

            response = await litellm.aembedding(model=model_name, input=texts, **kwargs)
            return [d["embedding"] for d in response["data"]]
        except Exception as e:
            print(f"LiteLLM embedding for {model_name} failed: {e}")
            # Return zeros to allow fusion to continue with other models
            return [[0.0] * dim for _ in texts]


class LocalEmbeddingProvider(IEmbeddingProvider):
    """Local embedding provider wrapping the embedding service."""

    def __init__(self, embedding_service: Any = None):
        self.service = embedding_service or get_embedding_service()

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        results = await self.service.generate_embeddings_async([text])
        return results[0] if results else []

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        return await self.service.generate_embeddings_async(texts)

    def get_dimension(self) -> int:
        """Get embedding dimension."""
        # Ensure we check availability to set use_litellm correctly
        self.service._ensure_available()

        # Check if using Ollama which usually has 768 dims for nomic-embed-text
        if self.service.use_litellm:
            if self.service.litellm_model.startswith("ollama/"):
                return 768

        # Default for all-MiniLM-L6-v2
        return 384


class RemoteEmbeddingProvider(IEmbeddingProvider):
    """Embedding provider that offloads to a remote ML service (e.g., Node1)."""

    def __init__(self, base_url: str, dimension: int = 384):
        self.base_url = base_url
        self.dimension = dimension

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text by calling remote service."""
        results = await self.embed_batch([text])
        return results[0] if results else []

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts by calling remote service."""
        from apps.memory_api.services.ml_service_client import MLServiceClient

        client = MLServiceClient(base_url=self.base_url)
        try:
            result = await client.generate_embeddings(texts)
            return cast(List[List[float]], result.get("embeddings", []))
        finally:
            await client.close()

    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.dimension


class TaskQueueEmbeddingProvider(IEmbeddingProvider):
    """Embedding provider that offloads by creating tasks in the Control Plane queue."""

    def __init__(self, task_repo: Any, dimension: int = 384, timeout_sec: int = 60):
        self.task_repo = task_repo
        self.dimension = dimension
        self.timeout_sec = timeout_sec

    async def embed_text(self, text: str) -> List[float]:
        results = await self.embed_batch([text])
        return results[0] if results else []

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Offload embedding generation to a compute node via Task Queue.
        Waits for the task to be completed.
        """
        # 1. Create task
        task_payload = {
            "texts": texts,
            "model": "all-MiniLM-L6-v2",
            "goal": "Generate embeddings for batch",
        }

        # We need a way to create the task.
        # This provider is initialized with task_repo (which might be raw pool or repo)
        # Assuming task_repo has create_task method
        from apps.memory_api.repositories.task_repository import TaskRepository

        if not isinstance(self.task_repo, TaskRepository):
            from apps.memory_api.repositories.task_repository import TaskRepository

            repo = TaskRepository(self.task_repo)
        else:
            repo = self.task_repo

        task = await repo.create_task(
            type="llm_inference",  # Node agent handles llm_inference by calling Ollama
            payload=task_payload,
            priority=10,
        )

        task_id = task.id

        # 2. Poll for result
        import asyncio
        import time

        start_time = time.time()
        while time.time() - start_time < self.timeout_sec:
            updated_task = await repo.get_task(task_id)
            if updated_task and updated_task.status == "COMPLETED":
                import json

                result_data = (
                    json.loads(updated_task.result)
                    if isinstance(updated_task.result, str)
                    else updated_task.result
                )
                if result_data is None:
                    result_data = {}
                return cast(List[List[float]], result_data.get("embeddings", []))
            elif updated_task and updated_task.status == "FAILED":
                raise RuntimeError(f"Task {task_id} failed: {updated_task.error}")

            await asyncio.sleep(1.0)

        raise TimeoutError(
            f"Embedding task {task_id} timed out after {self.timeout_sec}s"
        )

    def get_dimension(self) -> int:
        return self.dimension


# Singleton instance
embedding_service = EmbeddingService()


def get_embedding_service() -> EmbeddingService:
    return embedding_service
