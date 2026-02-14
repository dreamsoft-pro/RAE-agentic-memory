"""In-Memory vector store adapter for RAE-core.

Simple vector storage with cosine similarity search using NumPy.
Ideal for testing, development, and lightweight deployments.
"""

import asyncio
import sys
from collections import defaultdict
from typing import Any, cast
from uuid import UUID

# Robust NumPy import to avoid re-import warnings
if "numpy" in sys.modules:
    np = sys.modules["numpy"]  # pragma: no cover
else:  # pragma: no cover
    import numpy as np  # pragma: no cover

from rae_core.interfaces.vector import IVectorStore


class InMemoryVectorStore(IVectorStore):
    """In-memory implementation of IVectorStore using NumPy.

    Features:
    - Fast NumPy-based cosine similarity search
    - Thread-safe operations with asyncio.Lock
    - Metadata storage alongside vectors
    - Layer filtering support
    - Batch operations
    """

    def __init__(self) -> None:
        """Initialize in-memory vector store."""
        # Main storage: {memory_id: vector_data}
        # vector_data = {"embedding": np.array, "tenant_id": str, "metadata": dict}
        self._vectors: dict[UUID, dict[str, Any]] = {}

        # Indexes for fast lookups
        self._by_tenant: dict[str, set[UUID]] = defaultdict(set)
        self._by_agent: dict[tuple[str, str], set[UUID]] = defaultdict(set)
        self._by_layer: dict[tuple[str, str], set[UUID]] = defaultdict(set)
        self._by_project: dict[tuple[str, str], set[UUID]] = defaultdict(set)

        # Thread safety
        self._lock = asyncio.Lock()

    def _normalize(self, vec: np.ndarray) -> np.ndarray:
        """Normalize vector for cosine similarity (dot product)."""
        norm = np.linalg.norm(vec)
        if norm > 0:
            return vec / norm
        return vec

    async def store_vector(
        self,
        memory_id: UUID,
        embedding: list[float] | dict[str, list[float]],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Store a vector embedding."""
        async with self._lock:
            # Handle multi-vector: take first vector or specific 'default' key
            if isinstance(embedding, dict):
                # Simple strategy: prefer 'default' or 'dense', else first available
                vec_list = (
                    embedding.get("default")
                    or embedding.get("dense")
                    or next(iter(embedding.values()))
                )
            else:
                vec_list = embedding

            meta = metadata or {}
            vector_data = {
                "embedding": self._normalize(np.array(vec_list, dtype=np.float32)),
                "tenant_id": tenant_id,
                "metadata": meta,
            }

            self._vectors[memory_id] = vector_data
            self._by_tenant[tenant_id].add(memory_id)

            # Update indexes
            if "agent_id" in meta:
                self._by_agent[(tenant_id, meta["agent_id"])].add(memory_id)
            if "layer" in meta:
                self._by_layer[(tenant_id, meta["layer"])].add(memory_id)
            if "project" in meta:
                self._by_project[(tenant_id, meta["project"])].add(memory_id)

            return True

    async def search_similar(
        self,
        query_embedding: list[float],
        tenant_id: str,
        layer: str | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
        agent_id: str | None = None,
        session_id: str | None = None,
        filters: dict[str, Any] | None = None,
        project: str | None = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float]]:
        """Search for similar vectors using cosine similarity."""
        async with self._lock:
            # Narrow down candidates using indexes
            candidate_ids = self._by_tenant.get(tenant_id, set()).copy()

            if layer:
                candidate_ids &= self._by_layer.get((tenant_id, layer), set())
            if agent_id:
                candidate_ids &= self._by_agent.get((tenant_id, agent_id), set())
            if project:
                candidate_ids &= self._by_project.get((tenant_id, project), set())

            if not candidate_ids:
                return []

            # Normalize query vector
            query_vec = self._normalize(np.array(query_embedding, dtype=np.float32))

            # Calculate similarities (Vectorized using NumPy)
            # 1. Filter out candidate IDs that might have been deleted but still in index
            valid_ids = [mid for mid in candidate_ids if mid in self._vectors]
            if not valid_ids:
                return []

            # 2. Extract embeddings into a matrix
            embeddings = np.stack(
                [self._vectors[mid]["embedding"] for mid in valid_ids]
            )

            # 3. Calculate dot products (since they are normalized, this is cosine similarity)
            similarities = np.dot(embeddings, query_vec)

            # 4. Filter and build results
            results = []
            for i, mid in enumerate(valid_ids):
                similarity = float(similarities[i])

                # Metadata filtering (session_id, generic filters)
                metadata = self._vectors[mid]["metadata"]
                if session_id and metadata.get("session_id") != session_id:
                    continue

                if filters:
                    match = True
                    for k, v in filters.items():
                        if metadata.get(k) != v:
                            match = False
                            break
                    if not match:
                        continue

                if score_threshold is not None and similarity < score_threshold:
                    continue

                results.append((mid, similarity))

            # Sort by similarity (descending) and limit
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:limit]

    async def delete_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a vector."""
        async with self._lock:
            vector_data = self._vectors.get(memory_id)

            if not vector_data or vector_data["tenant_id"] != tenant_id:
                return False

            metadata = vector_data.get("metadata", {})

            # Remove from indexes
            self._by_tenant[tenant_id].discard(memory_id)
            if "agent_id" in metadata:
                self._by_agent[(tenant_id, metadata["agent_id"])].discard(memory_id)
            if "layer" in metadata:
                self._by_layer[(tenant_id, metadata["layer"])].discard(memory_id)
            if "project" in metadata:
                self._by_project[(tenant_id, metadata["project"])].discard(memory_id)

            # Remove vector
            del self._vectors[memory_id]

            return True

    async def update_vector(
        self,
        memory_id: UUID,
        embedding: list[float] | dict[str, list[float]],
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Update a vector embedding."""
        async with self._lock:
            vector_data = self._vectors.get(memory_id)

            if not vector_data or vector_data["tenant_id"] != tenant_id:
                return False

            old_metadata = vector_data.get("metadata", {})

            # Handle multi-vector
            if isinstance(embedding, dict):
                vec_list = (
                    embedding.get("default")
                    or embedding.get("dense")
                    or next(iter(embedding.values()))
                )
            else:
                vec_list = embedding

            # Update embedding
            vector_data["embedding"] = self._normalize(
                np.array(vec_list, dtype=np.float32)
            )

            # Update metadata and indexes if provided
            if metadata is not None:
                # Update agent index
                if "agent_id" in old_metadata:
                    self._by_agent[(tenant_id, old_metadata["agent_id"])].discard(
                        memory_id
                    )
                if "agent_id" in metadata:
                    self._by_agent[(tenant_id, metadata["agent_id"])].add(memory_id)

                # Update layer index
                if "layer" in old_metadata:
                    self._by_layer[(tenant_id, old_metadata["layer"])].discard(
                        memory_id
                    )
                if "layer" in metadata:
                    self._by_layer[(tenant_id, metadata["layer"])].add(memory_id)

                # Update project index
                if "project" in old_metadata:
                    self._by_project[(tenant_id, old_metadata["project"])].discard(
                        memory_id
                    )
                if "project" in metadata:
                    self._by_project[(tenant_id, metadata["project"])].add(memory_id)

                vector_data["metadata"] = metadata

            return True

    async def get_vector(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> list[float] | None:
        """Retrieve a vector embedding."""
        async with self._lock:
            vector_data = self._vectors.get(memory_id)

            if not vector_data or vector_data["tenant_id"] != tenant_id:
                return None

            # Convert numpy array back to list
            return cast(list[float], vector_data["embedding"].tolist())

    async def batch_store_vectors(
        self,
        vectors: list[
            tuple[UUID, list[float] | dict[str, list[float]], dict[str, Any]]
        ],
        tenant_id: str,
    ) -> int:
        """Store multiple vectors in a batch."""
        async with self._lock:
            count = 0

            for memory_id, embedding, metadata in vectors:
                try:
                    # Handle multi-vector
                    if isinstance(embedding, dict):
                        vec_list = (
                            embedding.get("default")
                            or embedding.get("dense")
                            or next(iter(embedding.values()))
                        )
                    else:
                        vec_list = embedding

                    meta = metadata or {}
                    vector_data = {
                        "embedding": self._normalize(
                            np.array(vec_list, dtype=np.float32)
                        ),
                        "tenant_id": tenant_id,
                        "metadata": meta,
                    }

                    self._vectors[memory_id] = vector_data
                    self._by_tenant[tenant_id].add(memory_id)

                    # Update indexes
                    if "agent_id" in meta:
                        self._by_agent[(tenant_id, meta["agent_id"])].add(memory_id)
                    if "layer" in meta:
                        self._by_layer[(tenant_id, meta["layer"])].add(memory_id)
                    if "project" in meta:
                        self._by_project[(tenant_id, meta["project"])].add(memory_id)

                    count += 1
                except Exception:
                    # Skip invalid vectors
                    continue

            return count

    async def search_similar_batch(
        self,
        query_embeddings: list[list[float]],
        tenant_id: str,
        layer: str | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
    ) -> list[list[tuple[UUID, float]]]:
        """Search for similar vectors for multiple queries.

        Args:
            query_embeddings: List of query vectors
            tenant_id: Tenant identifier
            layer: Optional layer filter
            limit: Maximum results per query
            score_threshold: Optional minimum similarity score

        Returns:
            List of result lists, one per query
        """
        results = []

        for query_embedding in query_embeddings:
            result = await self.search_similar(
                query_embedding=query_embedding,
                tenant_id=tenant_id,
                layer=layer,
                limit=limit,
                score_threshold=score_threshold,
            )
            results.append(result)

        return results

    async def clear_tenant(self, tenant_id: str) -> int:
        """Clear all vectors for a tenant.

        Args:
            tenant_id: Tenant identifier

        Returns:
            Number of vectors deleted
        """
        async with self._lock:
            memory_ids = self._by_tenant[tenant_id].copy()

            for memory_id in memory_ids:
                if memory_id in self._vectors:
                    metadata = self._vectors[memory_id].get("metadata", {})
                    # Remove from all indexes
                    if "agent_id" in metadata:
                        self._by_agent[(tenant_id, metadata["agent_id"])].discard(
                            memory_id
                        )
                    if "layer" in metadata:
                        self._by_layer[(tenant_id, metadata["layer"])].discard(
                            memory_id
                        )
                    if "project" in metadata:
                        self._by_project[(tenant_id, metadata["project"])].discard(
                            memory_id
                        )
                    del self._vectors[memory_id]

            del self._by_tenant[tenant_id]

            return len(memory_ids)

    async def get_statistics(self) -> dict[str, Any]:
        """Get vector store statistics.

        Returns:
            Dictionary with statistics
        """
        async with self._lock:
            total_vectors = len(self._vectors)
            tenants = len(self._by_tenant)

            # Calculate dimension distribution
            dimensions = set()
            for vector_data in self._vectors.values():
                dimensions.add(len(vector_data["embedding"]))

            return {
                "total_vectors": total_vectors,
                "tenants": tenants,
                "dimensions": sorted(dimensions) if dimensions else [],
            }

    async def clear_all(self) -> int:
        """Clear all data (use with caution!).

        Returns:
            Number of vectors deleted
        """
        async with self._lock:
            count = len(self._vectors)

            self._vectors.clear()
            self._by_tenant.clear()
            self._by_agent.clear()
            self._by_layer.clear()
            self._by_project.clear()

            return count
