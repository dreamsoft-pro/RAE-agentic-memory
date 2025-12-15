"""Abstract embedding provider interface for RAE-core."""

from abc import ABC, abstractmethod


class IEmbeddingProvider(ABC):
    """Abstract interface for embedding providers."""

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for text."""
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        pass
