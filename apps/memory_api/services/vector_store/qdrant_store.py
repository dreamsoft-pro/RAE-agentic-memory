import hashlib
import logging
from typing import TYPE_CHECKING, Any, Dict, List

import numpy as np
import structlog
from qdrant_client import QdrantClient, models
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Optional ML dependencies
try:  # pragma: no cover
    import onnxruntime

    ONNXRUNTIME_AVAILABLE = True
except ImportError:  # pragma: no cover
    onnxruntime = None  # type: ignore[assignment]
    ONNXRUNTIME_AVAILABLE = False

try:  # pragma: no cover
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:  # pragma: no cover
    SentenceTransformer = None  # type: ignore[assignment,misc]
    SENTENCE_TRANSFORMERS_AVAILABLE = False

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer  # noqa: F401

from ...config import settings
from ...metrics import vector_query_time_histogram
from ...models import MemoryRecord, ScoredMemoryRecord
from .base import MemoryVectorStore

logger = structlog.get_logger(__name__)


class QdrantStore(MemoryVectorStore):
    """
    A vector store implementation using Qdrant.
    """

    def __init__(self):
        self.qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST, port=settings.QDRANT_PORT
        )
        # self.embedding_model was removed as it is not used in QdrantStore.
        # Embeddings are passed explicitly to upsert/query methods.

        self.ensure_collection_exists()

    def ensure_collection_exists(self):
        """
        Ensures that the Qdrant collection exists with the correct configuration.
        Creates it if it doesn't exist. Supports Multi-Vector config.
        """
        collection_name = "memories"
        try:
            # Determine vector dimension from EmbeddingService
            from apps.memory_api.services.embedding import (
                LocalEmbeddingProvider,
                get_embedding_service,
            )

            try:
                embedding_service = get_embedding_service()
                provider = LocalEmbeddingProvider(embedding_service)
                dimension = provider.get_dimension()
            except Exception as e:
                logger.warning(
                    f"Could not determine embedding dimension from service: {e}. using default 384."
                )
                dimension = 384

            collections = self.qdrant_client.get_collections().collections
            exists = any(c.name == collection_name for c in collections)

            if not exists:
                logger.info(
                    f"Collection '{collection_name}' not found. Creating with Multi-Vector support..."
                )
                self.qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config={
                        "dense": models.VectorParams(
                            size=dimension,
                            distance=models.Distance.COSINE,
                        ),
                        # Additional vectors for Multi-Vector Fusion (MATH-2)
                        "openai": models.VectorParams(
                            size=1536,
                            distance=models.Distance.COSINE,
                        ),
                        "ollama": models.VectorParams(
                            size=384,
                            distance=models.Distance.COSINE,
                        ),
                    },
                    sparse_vectors_config={"text": models.SparseVectorParams()},
                )
                logger.info(f"Collection '{collection_name}' created successfully.")
            else:
                logger.debug(f"Collection '{collection_name}' already exists.")
                # TODO: Check if existing collection supports named vectors and migrate if needed
        except Exception as e:
            logger.error(f"Failed to ensure collection exists: {e}")
            # Don't raise here to allow app startup even if Qdrant is temporarily down
            # Retry logic in upsert/query will handle connection issues

    def _get_onnx_embedder(self, model_path: str):
        # This is a placeholder for a real ONNX embedder
        class OnnxEmbedder:
            def encode(self, texts: List[str]) -> np.ndarray:
                return np.random.rand(len(texts), 384).astype(np.float32)

        return OnnxEmbedder()

    def _get_sparse_vector(self, text: str) -> models.SparseVector:
        """
        Generates a simple sparse vector from text by hashing words.
        """
        words = text.lower().split()
        stopwords = {
            "a",
            "an",
            "the",
            "is",
            "in",
            "on",
            "of",
            "for",
            "to",
            "with",
            "and",
            "or",
            "but",
        }

        # Use dict to handle hash collisions and ensure unique indices
        index_values: Dict[int, float] = {}

        for word in set(words):
            if word not in stopwords:
                index = (
                    int(
                        hashlib.md5(word.encode(), usedforsecurity=False).hexdigest(),
                        16,
                    )
                    % 100000
                )
                # Accumulate values for duplicate indices (hash collisions)
                index_values[index] = index_values.get(index, 0.0) + 1.0

        # Convert to sorted lists for Qdrant
        indices = sorted(index_values.keys())
        values = [index_values[i] for i in indices]

        return models.SparseVector(indices=indices, values=values)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def upsert(self, memories: List[MemoryRecord], embeddings: List[Any]):
        """
        Upserts a list of memories into the Qdrant collection.

        Supports both simple List[float] (mapped to "dense") and
        Dict[str, List[float]] (mapped to named vectors).

        Implements retry logic with exponential backoff.
        """
        if len(memories) != len(embeddings):
            raise ValueError("The number of memories and embeddings must be the same.")

        try:
            points_to_upsert = []
            for memory, embedding in zip(memories, embeddings):
                sparse_vector = self._get_sparse_vector(memory.content)

                # Handle Multi-Vector input
                if isinstance(embedding, dict):
                    # It's a dictionary of named vectors
                    vector_payload = embedding
                    # Ensure "text" sparse vector is added
                    vector_payload["text"] = sparse_vector
                    # Ensure "dense" exists for backward compatibility if possible
                    if "dense" not in vector_payload and "ollama" in vector_payload:
                        vector_payload["dense"] = vector_payload["ollama"]  # Fallback
                else:
                    # Legacy: single list of floats
                    vector_payload = {
                        "dense": embedding,
                        "text": sparse_vector,
                    }

                points_to_upsert.append(
                    models.PointStruct(
                        id=str(memory.id),
                        vector=vector_payload,
                        payload=memory.model_dump(),
                    )
                )
            self.qdrant_client.upsert(
                collection_name="memories", points=points_to_upsert, wait=True
            )

            logger.info("qdrant_upsert_success", memory_count=len(memories))

        except Exception as e:
            logger.error(
                "qdrant_upsert_failed",
                error=str(e),
                memory_count=len(memories),
                memory_ids=[m.id for m in memories],
            )
            raise

    @vector_query_time_histogram.time()
    async def query(
        self,
        query_embedding: List[float],
        top_k: int,
        filters: Dict[str, Any],
        vector_name: str = "dense",
    ) -> List[ScoredMemoryRecord]:
        """
        Queries the Qdrant collection using a dense vector embedding.

        Args:
            query_embedding: Vector to search with
            top_k: Number of results
            filters: Search filters
            vector_name: Name of the vector to search ("dense", "openai", "ollama")
        """
        qdrant_filters = models.Filter(**filters) if filters else None

        search_results = self.qdrant_client.search(
            collection_name="memories",
            query_vector=models.NamedVector(name=vector_name, vector=query_embedding),
            query_filter=qdrant_filters,
            limit=top_k,
            with_payload=True,
        )

        return [
            ScoredMemoryRecord(score=point.score, **point.payload)
            for point in search_results
        ]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def delete(self, memory_id: str):
        """
        Deletes a memory from the Qdrant collection by its ID.

        Implements retry logic with exponential backoff.
        """
        try:
            self.qdrant_client.delete(
                collection_name="memories",
                points_selector=models.PointIdsList(points=[memory_id]),
            )

            logger.info("qdrant_delete_success", memory_id=memory_id)

        except Exception as e:
            logger.error("qdrant_delete_failed", error=str(e), memory_id=memory_id)
            raise
