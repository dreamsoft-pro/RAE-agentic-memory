"""Abstract vector store interface for RAE-core.

This module defines the vector store interface for similarity search.
Implementations can use Qdrant, sqlite-vec, FAISS, or any other vector DB.
"""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class IVectorStore(ABC):
    """Abstract interface for vector storage and similarity search.

    Implementations must provide vector storage and efficient similarity search
    capabilities for memory embeddings.
    """

    @abstractmethod
    async def store_vector(
        self,
        memory_id: UUID,
        embedding: list[float],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Store a vector embedding.

        Args:
            memory_id: UUID of the memory
            embedding: Vector embedding (typically 1536 dimensions for OpenAI)
            tenant_id: Tenant identifier
            metadata: Optional metadata to store with the vector

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def search_similar(
        self,
        query_embedding: list[float],
        tenant_id: str,
        layer: str | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
    ) -> list[tuple[UUID, float]]:
        """Search for similar vectors using cosine similarity.

        Args:
            query_embedding: Query vector
            tenant_id: Tenant identifier
            layer: Optional layer filter
            limit: Maximum number of results
            score_threshold: Optional minimum similarity score (0.0-1.0)

        Returns:
            List of (memory_id, similarity_score) tuples, sorted by score descending
        """
        pass

    @abstractmethod
    async def delete_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a vector.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def update_vector(
        self,
        memory_id: UUID,
        embedding: list[float],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Update a vector embedding.

        Args:
            memory_id: UUID of the memory
            embedding: New vector embedding
            tenant_id: Tenant identifier
            metadata: Optional new metadata

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> list[float] | None:
        """Retrieve a vector embedding.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier

        Returns:
            Vector embedding or None if not found
        """
        pass

    @abstractmethod
    async def batch_store_vectors(
        self,
        vectors: list[tuple[UUID, list[float], dict[str, Any]]],
        tenant_id: str,
    ) -> int:
        """Store multiple vectors in a batch.

        Args:
            vectors: List of (memory_id, embedding, metadata) tuples
            tenant_id: Tenant identifier

        Returns:
            Number of successfully stored vectors
        """
        pass
