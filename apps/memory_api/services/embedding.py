from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from apps.memory_api.config import settings
from apps.memory_api.metrics import embedding_time_histogram

# --- Embedding Model Loading ---
# This logic is moved from the old qdrant_client.py


class EmbeddingService:
    def __init__(self):
        if settings.ONNX_EMBEDDER_PATH:
            # Placeholder for a real ONNX embedder class
            # A real implementation would load the model and tokenizer here.
            # self.model = self._get_onnx_embedder(settings.ONNX_EMBEDDER_PATH)
            print(
                f"Using ONNX embedder (placeholder) from: {settings.ONNX_EMBEDDER_PATH}"
            )
            # For now, we fall back to SentenceTransformer even if ONNX path is set,
            # as the ONNX implementation is just a placeholder.
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        else:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("Using SentenceTransformer 'all-MiniLM-L6-v2'")

    @embedding_time_histogram.time()
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates dense embeddings for a list of texts.
        """
        embeddings = self.model.encode(texts)
        return [emb.tolist() for emb in embeddings]


# Singleton instance
embedding_service = EmbeddingService()


def get_embedding_service() -> EmbeddingService:
    return embedding_service
