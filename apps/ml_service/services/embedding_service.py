"""
Embedding Service - Local embedding generation using SentenceTransformers.

This service handles embedding generation for the ML microservice,
keeping heavy dependencies isolated from the main API.
"""

from typing import Any, List, cast

import structlog
from sentence_transformers import SentenceTransformer

logger = structlog.get_logger(__name__)


class EmbeddingMLService:
    """
    Service for generating embeddings using local SentenceTransformer models.

    This is a singleton service that loads the model once and reuses it
    for all embedding requests.
    """

    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding service with specified model.

        Args:
            model_name: Name of the SentenceTransformer model to use
        """
        if self._model is None:
            logger.info("loading_embedding_model", model_name=model_name)
            self._model = SentenceTransformer(model_name)
            logger.info("embedding_model_loaded", model_name=model_name)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        if not texts:
            return []

        logger.info("generating_embeddings", text_count=len(texts))

        # Generate embeddings using SentenceTransformer
        model = cast(SentenceTransformer, self._model)
        embeddings = model.encode(texts, show_progress_bar=False)

        # Convert numpy arrays to Python lists
        result = [emb.tolist() for emb in embeddings]

        logger.info(
            "embeddings_generated",
            text_count=len(texts),
            embedding_dim=len(result[0]) if result else 0,
        )

        return result

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model.

        Returns:
            Integer dimension of embedding vectors
        """
        dim = cast(SentenceTransformer, self._model).get_sentence_embedding_dimension()
        return int(dim or 0)
