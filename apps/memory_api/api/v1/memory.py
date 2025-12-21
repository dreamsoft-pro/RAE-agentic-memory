from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from apps.memory_api.dependencies import get_rae_core_service
from apps.memory_api.metrics import (
    memory_delete_counter,
    memory_query_counter,
    memory_store_counter,
)
from apps.memory_api.models import RebuildReflectionsRequest  # NEW
from apps.memory_api.models import (
    DeleteMemoryResponse,
    QueryMemoryRequest,
    QueryMemoryResponse,
    StoreMemoryRequest,
    StoreMemoryResponse,
)
from apps.memory_api.observability.rae_tracing import get_tracer
from apps.memory_api.security import auth
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services import pii_scrubber, scoring
from apps.memory_api.services.embedding import get_embedding_service  # NEW
from apps.memory_api.services.rae_core_service import RAECoreService
from apps.memory_api.services.vector_store import get_vector_store  # NEW
from apps.memory_api.tasks.background_tasks import (  # NEW
    generate_reflection_for_project,
)

logger = structlog.get_logger(__name__)
tracer = get_tracer(__name__)

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
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    Stores a new memory record in the database and vector store.

    **Security:** Requires authentication and tenant access with memories:write permission.
    """
    with tracer.start_as_current_span("rae.api.memory.store") as span:
        span.set_attribute("rae.tenant_id", tenant_id)
        if req.project:
            span.set_attribute("rae.project_id", req.project)
        span.set_attribute("rae.memory.content_length_original", len(req.content))
        span.set_attribute("rae.memory.importance", req.importance)
        if req.layer:
            span.set_attribute("rae.memory.layer", req.layer.value)
        if req.tags:
            span.set_attribute("rae.memory.tags_count", len(req.tags))
        span.set_attribute("rae.memory.source", req.source)

        content = pii_scrubber.scrub_text(req.content)
        span.set_attribute("rae.memory.content_length_scrubbed", len(content))

        try:
            # 1. Store metadata in Postgres using RAE-Core Service
            memory_id = await rae_service.store_memory(
                tenant_id=tenant_id,
                project=req.project,
                content=content,
                source=req.source,
                importance=req.importance,
                layer=req.layer.value if req.layer else None,
                tags=req.tags,
            )

            # RAE-Core Service handles vector storage internally now (via Engine)
            # But legacy API expected MemoryRecord object back or at least ID.
            # RAECoreService.store_memory returns ID string.

            span.set_attribute("rae.memory.id", str(memory_id))

        except HTTPException:
            raise
        except Exception as e:
            span.set_attribute("rae.outcome.label", "storage_error")
            raise HTTPException(status_code=500, detail=f"Storage error: {e}")

        span.set_attribute("rae.outcome.label", "success")
        memory_store_counter.labels(
            tenant_id=tenant_id
        ).inc()  # Increment store counter
        return StoreMemoryResponse(id=memory_id)


@router.post("/query", response_model=QueryMemoryResponse)
async def query_memory(
    req: QueryMemoryRequest,
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    Queries the memory for relevant records based on a query text.

    Supports vector search.

    Args:
        req: Query request parameters
        request: FastAPI request object
        tenant_id: Verified tenant ID (injected via RBAC)
        rae_service: RAECoreService (injected via DI)

    **Security:** Requires authentication and tenant access with memories:read permission.
    """
    with tracer.start_as_current_span("rae.api.memory.query") as span:
        span.set_attribute("rae.tenant_id", tenant_id)
        if req.project:
            span.set_attribute("rae.project_id", req.project)
        span.set_attribute("rae.query.text_length", len(req.query_text))
        span.set_attribute("rae.query.k", req.k)
        span.set_attribute(
            "rae.query.use_graph", req.use_graph
        )  # Still in request model
        if req.use_graph:
            span.set_attribute(
                "rae.query.graph_depth", req.graph_depth or 1
            )  # Still in request model
        if req.filters:
            span.set_attribute("rae.query.filters_count", len(req.filters))

        # Standard vector search
        span.set_attribute("rae.query.mode", "vector_only")

        # Get embedding service
        embedding_service = get_embedding_service()

        # Get query embedding for vector search
        query_embedding = (embedding_service.generate_embeddings([req.query_text]))[0]
        span.set_attribute("rae.query.embedding_dimension", len(query_embedding))

        # 2. Build filters
        # This part needs to be adapted to be backend-agnostic.
        # For now, we'll create a dictionary that can be interpreted by the stores.
        query_filters = {"must": [{"key": "tenant_id", "match": {"value": tenant_id}}]}
        if req.filters:
            # A more robust implementation would map API filters to backend-specific filters.
            # This is a simplified example.
            for key, value in req.filters.items():
                if key == "tags" and isinstance(value, list):
                    query_filters["must"].append(
                        {"key": "tags", "match": {"any": value}}
                    )

        # 3. Query the vector store
        try:
            vector_store = get_vector_store(pool=request.app.state.pool)
            raw_results = await vector_store.query(
                query_embedding=query_embedding,
                top_k=req.k,
                filters=query_filters,
            )
            span.set_attribute("rae.query.raw_results_count", len(raw_results))
        except Exception as e:
            span.set_attribute("rae.outcome.label", "vector_store_query_error")
            raise HTTPException(
                status_code=502, detail=f"Vector store query error: {e}"
            )

        # 4. Rescore memories using additional heuristics (optional)
        rescored_results = scoring.rescore_memories(raw_results)
        span.set_attribute("rae.query.rescored_results_count", len(rescored_results))

        # 5. Update access statistics for retrieved memories
        memory_ids = [item.id for item in rescored_results]
        if memory_ids:
            try:
                await rae_service.update_memory_access_batch(
                    memory_ids=memory_ids, tenant_id=tenant_id
                )
            except Exception as e:
                # Log but don't fail the query
                logger.warning(
                    "vector_query_access_stats_update_failed",
                    tenant_id=tenant_id,
                    error=str(e),
                )

        span.set_attribute("rae.outcome.label", "success")
        memory_query_counter.labels(
            tenant_id=tenant_id
        ).inc()  # Increment query counter
        return QueryMemoryResponse(results=rescored_results)


@router.delete("/delete", response_model=DeleteMemoryResponse)
async def delete_memory(
    memory_id: str,
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    Deletes a memory record from the database and vector store.

    **Security:** Requires authentication and tenant access with memories:delete permission.
    """
    with tracer.start_as_current_span("rae.api.memory.delete") as span:
        span.set_attribute("rae.tenant_id", tenant_id)
        span.set_attribute("rae.memory.id", memory_id)

        # 1. Delete from database using RAE-Core Service
        try:
            deleted = await rae_service.delete_memory(memory_id, tenant_id)

            if not deleted:
                span.set_attribute("rae.outcome.label", "not_found")
                raise HTTPException(status_code=404, detail="Memory not found.")

            span.set_attribute("rae.memory.db_deleted", True)

        except HTTPException:
            raise
        except Exception as e:
            span.set_attribute("rae.outcome.label", "database_error")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        # 2. Delete from vector store - HANDLED BY RAE-CORE ENGINE via DELETE_MEMORY
        # Assuming RAE-Core engine handles both storage and vector store deletion.
        # RAECoreService.delete_memory calls storage adapter.
        # If vector store is separate in engine, engine.delete_memory should be called instead of adapter directly.
        # RAECoreService.delete_memory wraps adapter.delete_memory currently (based on previous edits).
        # ideally RAECoreService.delete_memory should call engine.delete_memory.
        # Checking RAECoreService implementation:
        # async def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        #     try:
        #         mem_uuid = UUID(memory_id)
        #     except ValueError:
        #         return False
        #     return await self.postgres_adapter.delete_memory(mem_uuid, tenant_id)

        # It calls adapter directly. So vector store deletion is NOT handled by RAECoreService yet if engine is not used.
        # To maintain vector store deletion, we should use RAEEngine if possible or keep explicit vector store delete.
        # Given we want to move logic to RAECore, RAEEngine should be used.
        # But RAECoreService wraps Engine and Adapters.

        # Let's keep manual vector delete for now to be safe, or assume Engine handles it if we used engine.delete_memory.
        # But RAECoreService.delete_memory uses adapter.
        # Let's keep explicit vector delete for safety until Engine handles it fully.

        try:
            vector_store = get_vector_store(pool=request.app.state.pool)
            await vector_store.delete(memory_id)
            span.set_attribute("rae.memory.vector_deleted", True)
        except Exception as e:
            # Log the error but don't fail the request, as the DB part succeeded.
            logger.warning(
                "vector_store_deletion_failed", memory_id=memory_id, error=str(e)
            )
            span.set_attribute("rae.memory.vector_deleted", False)
            span.set_attribute("rae.memory.vector_delete_error", str(e))

        span.set_attribute("rae.outcome.label", "success")
        memory_delete_counter.labels(
            tenant_id=tenant_id
        ).inc()  # Increment delete counter
        return DeleteMemoryResponse(message=f"Memory {memory_id} deleted successfully.")


@router.post("/rebuild-reflections", status_code=202)
async def rebuild_reflections(req: RebuildReflectionsRequest):
    """
    Triggers a background task to rebuild reflections for a specific project.
    """
    with tracer.start_as_current_span("rae.api.memory.rebuild_reflections") as span:
        span.set_attribute("rae.tenant_id", req.tenant_id)
        span.set_attribute("rae.project_id", req.project)
        span.set_attribute("rae.task.type", "background")

        generate_reflection_for_project.delay(
            project=req.project, tenant_id=req.tenant_id
        )

        span.set_attribute("rae.outcome.label", "task_dispatched")
        return {
            "message": f"Reflection rebuild task dispatched for project {req.project}."
        }


@router.get("/reflection-stats")
async def get_reflection_stats(
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
    project: Optional[str] = None,
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    Gets statistics about reflective memories.

    **Security:** Requires authentication and tenant access.
    """
    with tracer.start_as_current_span("rae.api.memory.reflection_stats") as span:
        span.set_attribute("rae.tenant_id", tenant_id)
        if project:
            span.set_attribute("rae.project_id", project)

        count = await rae_service.count_memories(
            tenant_id=tenant_id, layer="rm", project=project or "default"
        )
        span.set_attribute("rae.reflection.count", count)

        avg_strength = await rae_service.get_metric_aggregate(
            tenant_id=tenant_id,
            layer="rm",
            project=project or "default",
            metric="importance",
            func="avg",
        )
        span.set_attribute("rae.reflection.avg_strength", avg_strength or 0.0)

        span.set_attribute("rae.outcome.label", "success")
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
    rae_service: RAECoreService = Depends(get_rae_core_service),
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
    with tracer.start_as_current_span(
        "rae.api.memory.hierarchical_reflection_deprecated"
    ) as span:
        tenant_id = request.headers.get("X-Tenant-Id")
        if not tenant_id:
            span.set_attribute("rae.outcome.label", "missing_tenant_id")
            raise HTTPException(
                status_code=400, detail="X-Tenant-Id header is required."
            )

        span.set_attribute("rae.tenant_id", tenant_id)
        span.set_attribute("rae.project_id", project)
        span.set_attribute("rae.reflection.bucket_size", bucket_size)
        if max_episodes:
            span.set_attribute("rae.reflection.max_episodes", max_episodes)
        span.set_attribute("rae.api.deprecated", True)

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
            reflection_engine = ReflectionEngine(request.app.state.pool, rae_service)

            # Generate hierarchical reflection
            summary = await reflection_engine.generate_hierarchical_reflection(
                project=project,
                tenant_id=tenant_id,
                bucket_size=bucket_size,
                max_episodes=max_episodes,
            )
            span.set_attribute("rae.reflection.summary_length", len(summary))

            # Fetch statistics using RAECoreService
            episode_count = await rae_service.count_memories(
                tenant_id=tenant_id, layer="em", project=project
            )
            span.set_attribute("rae.reflection.episode_count", episode_count)

            logger.info(
                "hierarchical_reflection_completed_deprecated",
                tenant_id=tenant_id,
                project=project,
                episode_count=episode_count,
                summary_length=len(summary),
            )

            span.set_attribute("rae.outcome.label", "success")
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
            span.set_attribute("rae.outcome.label", "generation_failed")
            raise HTTPException(
                status_code=500,
                detail=f"Hierarchical reflection generation failed: {str(e)}",
            )
