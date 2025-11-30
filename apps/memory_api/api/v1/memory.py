from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from apps.memory_api.dependencies import get_hybrid_search_service  # NEW
from apps.memory_api.metrics import (
    memory_delete_counter,
    memory_query_counter,
    memory_store_counter,
)
from apps.memory_api.models import MemoryRecord  # NEW
from apps.memory_api.models import RebuildReflectionsRequest  # NEW
from apps.memory_api.models import (
    DeleteMemoryResponse,
    QueryMemoryRequest,
    QueryMemoryResponse,
    StoreMemoryRequest,
    StoreMemoryResponse,
)
from apps.memory_api.repositories.memory_repository import MemoryRepository  # NEW
from apps.memory_api.security import auth
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services import pii_scrubber, scoring
from apps.memory_api.services.embedding import get_embedding_service  # NEW
from apps.memory_api.services.hybrid_search import HybridSearchService  # NEW
from apps.memory_api.services.vector_store import get_vector_store  # NEW
from apps.memory_api.tasks.background_tasks import (  # NEW
    generate_reflection_for_project,
)

logger = structlog.get_logger(__name__)

# All memory endpoints require authentication
router = APIRouter(
    prefix="/memory",
    tags=["memory-protocol"],
    dependencies=[Depends(auth.verify_token)],
)


@router.post("/store", response_model=StoreMemoryResponse)
async def store_memory(
    req: StoreMemoryRequest,
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
):
    """
    Stores a new memory record in the database and vector store.

    **Security:** Requires authentication and tenant access with memories:write permission.
    """

    content = pii_scrubber.scrub_text(req.content)

    try:
        # 1. Store metadata in Postgres using repository
        memory_repository = MemoryRepository(request.app.state.pool)

        row_data = await memory_repository.insert_memory(
            tenant_id=tenant_id,
            content=content,
            source=req.source,
            importance=req.importance,
            layer=req.layer.value if req.layer else None,
            tags=req.tags,
            timestamp=req.timestamp,
            project=req.project,
        )

        if not row_data:
            raise HTTPException(
                status_code=500, detail="Failed to store memory in database."
            )

        memory_record = MemoryRecord(
            id=row_data["id"],
            tenant_id=tenant_id,
            content=content,
            source=req.source,
            importance=req.importance,
            layer=req.layer,
            tags=req.tags,
            timestamp=row_data["created_at"],
            last_accessed_at=row_data["last_accessed_at"],
            usage_count=row_data["usage_count"],
            project=req.project,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    try:
        # 2. Generate embedding
        embedding_service = get_embedding_service()
        embedding = embedding_service.generate_embeddings([content])[0]

        # 3. Upsert to vector store
        vector_store = get_vector_store(pool=request.app.state.pool)
        await vector_store.upsert([memory_record], [embedding])

    except Exception as e:
        # Here you might want to handle the case where the DB insert succeeded
        # but the vector store upsert failed (e.g., by scheduling a retry).
        # For now, we'll just raise an error.
        raise HTTPException(status_code=502, detail=f"Vector store error: {e}")

    memory_store_counter.labels(tenant_id=tenant_id).inc()  # Increment store counter
    return StoreMemoryResponse(id=memory_record.id)


@router.post("/query", response_model=QueryMemoryResponse)
async def query_memory(
    req: QueryMemoryRequest,
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
    hybrid_search: HybridSearchService = Depends(get_hybrid_search_service),
):
    """
    Queries the memory for relevant records based on a query text.

    Supports two modes:
    1. Standard vector search (use_graph=False)
    2. Hybrid search with graph traversal (use_graph=True)

    Hybrid search combines semantic similarity with knowledge graph relationships
    to provide richer, more contextual results.

    Args:
        req: Query request parameters
        request: FastAPI request object
        tenant_id: Verified tenant ID (injected via RBAC)
        hybrid_search: HybridSearchService (injected via DI)

    **Security:** Requires authentication and tenant access with memories:read permission.
    """

    # Check if hybrid search is requested
    if req.use_graph:
        # Validate project parameter for graph search
        if not req.project:
            raise HTTPException(
                status_code=400,
                detail="project parameter is required when use_graph=True",
            )

        logger.info(
            "hybrid_search_requested",
            tenant_id=tenant_id,
            project=req.project,
            graph_depth=req.graph_depth,
        )

        try:
            # Use injected hybrid search service

            # Perform hybrid search
            hybrid_result = await hybrid_search.search(
                query=req.query_text,
                tenant_id=tenant_id,
                project_id=req.project,
                top_k_vector=req.k,
                graph_depth=req.graph_depth,
                use_graph=True,
                filters=req.filters,
            )

            # Rescore vector results
            rescored_results = scoring.rescore_memories(hybrid_result.vector_matches)

            # Update access statistics for retrieved memories
            memory_ids = [item.id for item in rescored_results]
            if memory_ids:
                try:
                    memory_repository = MemoryRepository(request.app.state.pool)
                    await memory_repository.update_memory_access_stats(
                        memory_ids=memory_ids, tenant_id=tenant_id
                    )
                except Exception as e:
                    # Log but don't fail the query
                    logger.warning(
                        "hybrid_query_access_stats_update_failed",
                        tenant_id=tenant_id,
                        error=str(e),
                    )

            memory_query_counter.labels(tenant_id=tenant_id).inc()

            return QueryMemoryResponse(
                results=rescored_results,
                synthesized_context=hybrid_result.synthesized_context,
                graph_statistics=hybrid_result.statistics,
            )

        except Exception as e:
            logger.exception("hybrid_search_failed", tenant_id=tenant_id, error=str(e))
            raise HTTPException(status_code=502, detail=f"Hybrid search error: {e}")

    # Standard vector search (original implementation)
    # 1. Generate embedding for the query text
    embedding_service = get_embedding_service()
    query_embedding = embedding_service.generate_embeddings([req.query_text])[0]

    # 2. Build filters
    # This part needs to be adapted to be backend-agnostic.
    # For now, we'll create a dictionary that can be interpreted by the stores.
    query_filters = {"must": [{"key": "tenant_id", "match": {"value": tenant_id}}]}
    if req.filters:
        # A more robust implementation would map API filters to backend-specific filters.
        # This is a simplified example.
        for key, value in req.filters.items():
            if key == "tags" and isinstance(value, list):
                query_filters["must"].append({"key": "tags", "match": {"any": value}})

    # 3. Query the vector store
    try:
        vector_store = get_vector_store(pool=request.app.state.pool)
        raw_results = await vector_store.query(
            query_embedding=query_embedding,
            top_k=req.k,
            filters=query_filters,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Vector store query error: {e}")

    # 4. Rescore memories using additional heuristics (optional)
    rescored_results = scoring.rescore_memories(raw_results)

    # 5. Update access statistics for retrieved memories
    memory_ids = [item.id for item in rescored_results]
    if memory_ids:
        try:
            memory_repository = MemoryRepository(request.app.state.pool)
            await memory_repository.update_memory_access_stats(
                memory_ids=memory_ids, tenant_id=tenant_id
            )
        except Exception as e:
            # Log but don't fail the query
            logger.warning(
                "vector_query_access_stats_update_failed",
                tenant_id=tenant_id,
                error=str(e),
            )

    memory_query_counter.labels(tenant_id=tenant_id).inc()  # Increment query counter
    return QueryMemoryResponse(results=rescored_results)


@router.delete("/delete", response_model=DeleteMemoryResponse)
async def delete_memory(
    memory_id: str,
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
):
    """
    Deletes a memory record from the database and vector store.

    **Security:** Requires authentication and tenant access with memories:delete permission.
    """

    # 1. Delete from database using repository
    try:
        memory_repository = MemoryRepository(request.app.state.pool)
        deleted = await memory_repository.delete_memory(memory_id, tenant_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Memory not found.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # 2. Delete from vector store
    try:
        vector_store = get_vector_store(pool=request.app.state.pool)
        await vector_store.delete(memory_id)
    except Exception as e:
        # Log the error but don't fail the request, as the DB part succeeded.
        # The record will be out of sync, but this is a decision to make.
        # For now, we'll just log it.
        print(f"Vector store deletion error: {e}")

    memory_delete_counter.labels(tenant_id=tenant_id).inc()  # Increment delete counter
    return DeleteMemoryResponse(message=f"Memory {memory_id} deleted successfully.")


@router.post("/rebuild-reflections", status_code=202)
async def rebuild_reflections(req: RebuildReflectionsRequest):
    """
    Triggers a background task to rebuild reflections for a specific project.
    """
    generate_reflection_for_project.delay(project=req.project, tenant_id=req.tenant_id)
    return {"message": f"Reflection rebuild task dispatched for project {req.project}."}


@router.get("/reflection-stats")
async def get_reflection_stats(
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
    project: Optional[str] = None,
):
    """
    Gets statistics about reflective memories.

    **Security:** Requires authentication and tenant access.
    """

    memory_repository = MemoryRepository(request.app.state.pool)

    count = await memory_repository.count_memories_by_layer(
        tenant_id=tenant_id, layer="rm", project=project
    )

    avg_strength = await memory_repository.get_average_strength(
        tenant_id=tenant_id, layer="rm", project=project
    )

    return {"reflective_memory_count": count, "average_strength": avg_strength}


@router.post("/reflection/hierarchical", deprecated=True)
async def generate_hierarchical_reflection(
    request: Request,
    project: str = Query(..., description="Project identifier"),
    bucket_size: int = Query(
        10, description="Number of episodes per bucket", ge=1, le=100
    ),
    max_episodes: Optional[int] = Query(
        None, description="Maximum episodes to process", ge=1
    ),
):
    """
    **DEPRECATED:** Use `/v1/graph/reflection/hierarchical` instead.

    This endpoint is deprecated and maintained only for backward compatibility.
    The canonical implementation is now in the Graph API at:
    `POST /v1/graph/reflection/hierarchical`

    The Graph API version uses proper Pydantic models and is better integrated
    with GraphRAG features.

    **Migration:**
    Instead of:
    ```
    POST /v1/memory/reflection/hierarchical?project=my-project&bucket_size=15
    ```

    Use:
    ```
    POST /v1/graph/reflection/hierarchical
    Content-Type: application/json

    {
      "project_id": "my-project",
      "bucket_size": 15
    }
    ```

    This endpoint will be removed in a future version.
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id header is required.")

    logger.warning(
        "deprecated_endpoint_used",
        endpoint="/v1/memory/reflection/hierarchical",
        tenant_id=tenant_id,
        message="Use /v1/graph/reflection/hierarchical instead",
    )

    try:
        # Import ReflectionEngine
        from apps.memory_api.services.reflection_engine import ReflectionEngine

        # Initialize reflection engine
        reflection_engine = ReflectionEngine(request.app.state.pool)

        # Generate hierarchical reflection
        summary = await reflection_engine.generate_hierarchical_reflection(
            project=project,
            tenant_id=tenant_id,
            bucket_size=bucket_size,
            max_episodes=max_episodes,
        )

        # Fetch statistics using repository
        memory_repository = MemoryRepository(request.app.state.pool)
        episode_count = await memory_repository.count_memories_by_layer(
            tenant_id=tenant_id, layer="em", project=project
        )

        logger.info(
            "hierarchical_reflection_completed_deprecated",
            tenant_id=tenant_id,
            project=project,
            episode_count=episode_count,
            summary_length=len(summary),
        )

        return {
            "summary": summary,
            "statistics": {
                "project": project,
                "tenant_id": tenant_id,
                "episode_count": episode_count,
                "bucket_size": bucket_size,
                "max_episodes_processed": max_episodes or episode_count,
                "summary_length": len(summary),
            },
        }

    except Exception as e:
        logger.exception(
            "hierarchical_reflection_failed",
            tenant_id=tenant_id,
            project=project,
            error=str(e),
        )
        raise HTTPException(
            status_code=500,
            detail=f"Hierarchical reflection generation failed: {str(e)}",
        )
