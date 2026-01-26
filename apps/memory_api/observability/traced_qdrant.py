"""
Traced Qdrant Client Wrapper - Async Version

This module provides OpenTelemetry tracing for Qdrant operations.
Since Qdrant doesn't have native OTEL instrumentation, this wrapper
adds custom spans for all vector database operations.
"""

import time
from contextlib import asynccontextmanager
from typing import Any, List, Optional, cast, Tuple

import structlog
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, PointStruct, ScoredPoint, SearchParams

from .opentelemetry_config import OPENTELEMETRY_AVAILABLE, get_tracer

logger = structlog.get_logger(__name__)


class TracedQdrantClient:
    """
    Wrapper around AsyncQdrantClient that adds OpenTelemetry tracing.
    """

    def __init__(self, *args, **kwargs):
        """Initialize traced Qdrant client."""
        self.client = AsyncQdrantClient(*args, **kwargs)
        self.tracer = get_tracer("rae.qdrant") if OPENTELEMETRY_AVAILABLE else None

    @asynccontextmanager
    async def _trace_operation(
        self,
        operation: str,
        collection: Optional[str] = None,
        **attributes,
    ):
        """
        Create a span for a Qdrant operation.
        """
        if not self.tracer:
            yield None
            return

        start_time = time.time()

        with self.tracer.start_as_current_span(f"qdrant.{operation}") as span:
            span.set_attribute("qdrant.operation", operation)
            if collection:
                span.set_attribute("qdrant.collection", collection)

            for key, value in attributes.items():
                if value is not None:
                    span.set_attribute(f"qdrant.{key}", value)

            try:
                yield span
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.type", type(e).__name__)
                span.set_attribute("error.message", str(e))
                span.record_exception(e)
                raise
            finally:
                latency_ms = (time.time() - start_time) * 1000
                span.set_attribute("qdrant.latency_ms", round(latency_ms, 2))

    # ============================================================================
    # Collection Operations
    # ============================================================================

    async def create_collection(self, collection_name: str, *args, **kwargs):
        async with self._trace_operation("create_collection", collection=collection_name):
            return await self.client.create_collection(collection_name, *args, **kwargs)

    async def delete_collection(self, collection_name: str, **kwargs):
        async with self._trace_operation("delete_collection", collection=collection_name):
            return await self.client.delete_collection(collection_name, **kwargs)

    async def get_collection(self, collection_name: str):
        async with self._trace_operation("get_collection", collection=collection_name):
            return await self.client.get_collection(collection_name)

    async def collection_exists(self, collection_name: str) -> bool:
        async with self._trace_operation("collection_exists", collection=collection_name):
            return await self.client.collection_exists(collection_name)

    async def get_collections(self):
        async with self._trace_operation("get_collections"):
            return await self.client.get_collections()

    # ============================================================================
    # Point Operations
    # ============================================================================

    async def upsert(
        self,
        collection_name: str,
        points: List[PointStruct],
        wait: bool = True,
        **kwargs,
    ):
        async with self._trace_operation(
            "upsert",
            collection=collection_name,
            vector_count=len(points),
            wait=wait,
        ):
            return await self.client.upsert(
                collection_name=collection_name,
                points=points,
                wait=wait,
                **kwargs,
            )

    async def search(
        self,
        collection_name: str,
        query_vector: Any,
        limit: int = 10,
        query_filter: Optional[Filter] = None,
        search_params: Optional[SearchParams] = None,
        **kwargs,
    ) -> List[ScoredPoint]:
        async with self._trace_operation(
            "search",
            collection=collection_name,
            limit=limit,
            has_filter=query_filter is not None,
        ) as span:
            results = await self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=query_filter,
                search_params=search_params,
                **kwargs,
            )
            if span:
                span.set_attribute("qdrant.results_count", len(results))
            return results

    async def retrieve(
        self,
        collection_name: str,
        ids: List[str],
        with_vectors: bool = False,
        **kwargs,
    ):
        async with self._trace_operation(
            "retrieve",
            collection=collection_name,
            ids_count=len(ids),
            with_vectors=with_vectors,
        ):
            return await self.client.retrieve(
                collection_name=collection_name,
                ids=ids,
                with_vectors=with_vectors,
                **kwargs,
            )

    async def delete(
        self,
        collection_name: str,
        points_selector: Any,
        wait: bool = True,
        **kwargs,
    ):
        async with self._trace_operation("delete", collection=collection_name, wait=wait):
            return await self.client.delete(
                collection_name=collection_name,
                points_selector=points_selector,
                wait=wait,
                **kwargs,
            )

    async def scroll(
        self,
        collection_name: str,
        scroll_filter: Optional[Filter] = None,
        limit: int = 10,
        with_vectors: bool = False,
        **kwargs,
    ) -> Tuple[List[Any], Optional[Any]]:
        async with self._trace_operation(
            "scroll",
            collection=collection_name,
            limit=limit,
            has_filter=scroll_filter is not None,
            with_vectors=with_vectors,
        ) as span:
            results, next_page = await self.client.scroll(
                collection_name=collection_name,
                scroll_filter=scroll_filter,
                limit=limit,
                with_vectors=with_vectors,
                **kwargs,
            )
            if span:
                span.set_attribute("qdrant.results_count", len(results))
            return results, next_page

    async def count(
        self,
        collection_name: str,
        count_filter: Optional[Filter] = None,
        exact: bool = True,
        **kwargs,
    ) -> int:
        async with self._trace_operation(
            "count",
            collection=collection_name,
            has_filter=count_filter is not None,
            exact=exact,
        ) as span:
            result = await self.client.count(
                collection_name=collection_name,
                count_filter=count_filter,
                exact=exact,
                **kwargs,
            )
            count = result.count if hasattr(result, "count") else result
            if span:
                span.set_attribute("qdrant.count", count)
            return cast(int, count)

    def __getattr__(self, name):
        return getattr(self.client, name)


def create_traced_client(*args, **kwargs) -> TracedQdrantClient:
    return TracedQdrantClient(*args, **kwargs)