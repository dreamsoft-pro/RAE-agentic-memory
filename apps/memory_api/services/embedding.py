from typing import TYPE_CHECKING, List, Optional

from apps.memory_api.config import settings
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
    def __init__(self):
        self.model: Optional["SentenceTransformer"] = None
        self._initialized = False

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

        if settings.ONNX_EMBEDDER_PATH:
            # Placeholder for a real ONNX embedder class
            # A real implementation would load the model and tokenizer here.
            # self.model = self._get_onnx_embedder(settings.ONNX_EMBEDDER_PATH)
            print(
                f"Using ONNX embedder (placeholder) from: {settings.ONNX_EMBEDDER_PATH}"
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
        Generates dense embeddings for a list of texts.
        """
        self._initialize_model()
        embeddings = self.model.encode(texts)  # type: ignore[union-attr]
        return [emb.tolist() for emb in embeddings]


# Singleton instance
embedding_service = EmbeddingService()


def get_embedding_service() -> EmbeddingService:
    return embedding_service
