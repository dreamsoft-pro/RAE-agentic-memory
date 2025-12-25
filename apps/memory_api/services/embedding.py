from typing import TYPE_CHECKING, Any, List, Optional

from apps.memory_api.metrics import embedding_time_histogram

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

    @property
    def settings(self):
        from apps.memory_api.config import settings as default_settings

        return self._settings or default_settings

    def _ensure_available(self) -> None:
        """Ensure sentence-transformers is available."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise RuntimeError(
                "Embedding service requires sentence-transformers. "
                "Install ML extras or run: `pip install sentence-transformers`."
            )

    def _initialize_model(self) -> None:
        """Lazy initialization of the embedding model."""
        if self._initialized:
            return

        self._ensure_available()

        if self.settings.ONNX_EMBEDDER_PATH:
            # Placeholder for a real ONNX embedder class
            # A real implementation would load the model and tokenizer here.
            # self.model = self._get_onnx_embedder(self.settings.ONNX_EMBEDDER_PATH)
            print(
                f"Using ONNX embedder (placeholder) from: {self.settings.ONNX_EMBEDDER_PATH}"
            )
            # For now, we fall back to SentenceTransformer even if ONNX path is set,
            # as the ONNX implementation is just a placeholder.
            self.model = SentenceTransformer("all-MiniLM-L6-v2")  # type: ignore[misc]
        else:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")  # type: ignore[misc]
            print("Using SentenceTransformer 'all-MiniLM-L6-v2'")

        self._initialized = True

    @embedding_time_histogram.time()
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates dense embeddings for a list of texts (synchronous).
        """
        self._initialize_model()
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
                return result.get("embeddings", [])
            finally:
                await client.close()

        # Fallback to local execution (offloaded to thread pool if needed,
        # but here we just call the sync version for simplicity)
        import asyncio

        return await asyncio.to_thread(self.generate_embeddings, texts)


# Singleton instance
embedding_service = EmbeddingService()


def get_embedding_service() -> EmbeddingService:
    return embedding_service
