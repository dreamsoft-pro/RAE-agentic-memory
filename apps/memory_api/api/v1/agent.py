import httpx
import structlog
from fastapi import APIRouter, Depends, HTTPException, Request

from apps.memory_api.config import settings
from apps.memory_api.metrics import reflection_event_counter
from apps.memory_api.models import (
    AgentExecuteRequest,
    AgentExecuteResponse,
    CostInfo,
    QueryMemoryResponse,
    ScoredMemoryRecord,
    StoreMemoryRequest,
)
from apps.memory_api.security import auth
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services.context_builder import (  # NEW
    ContextBuilder,
    ContextConfig,
)
from apps.memory_api.services.embedding import get_embedding_service  # NEW
from apps.memory_api.services.llm import get_llm_provider  # NEW import
from apps.memory_api.services.llm.base import LLMResult  # NEW import - for type hinting
from apps.memory_api.services.token_estimator import estimate_tokens  # NEW
from apps.memory_api.services.vector_store import get_vector_store  # NEW
from apps.memory_api.utils.cost_tracker import track_request_cost  # NEW

# All agent endpoints require authentication
router = APIRouter(
    prefix="/agent",
    tags=["agent", "external"],
    dependencies=[Depends(auth.verify_token)],
)

logger = structlog.get_logger(__name__)


@router.post("/execute", response_model=AgentExecuteResponse)
async def execute(
    req: AgentExecuteRequest,
    request: Request,
    verified_tenant_id: str = Depends(get_and_verify_tenant_id),
):
    """
    Pipeline agenta:
    1) Retrieve z Qdrant (hybrid_search)
    2) Rerank przez reranker-service
    3) Budowa finalnego promptu
    4) Wywołanie LLM przez litellm
    5) Reflection hook - zapisanie refleksji jako nowego wspomnienia
    6) Zwrócenie odpowiedzi + użytych memories + kosztu

    **Security:** Requires authentication and tenant access.
    """

    # Use verified tenant_id from RBAC, or fall back to request tenant_id
    tenant_id = req.tenant_id or verified_tenant_id

    # 1. Build context using ContextBuilder (includes reflective memory)
    context_builder = ContextBuilder(
        pool=request.app.state.pool,
        config=ContextConfig(
            max_total_tokens=8000,
            max_reflections_tokens=1024,
            max_ltm_items=10,
            enable_enhanced_scoring=True,
        ),
    )

    # Build complete context with reflections
    working_memory = await context_builder.build_context(
        tenant_id=tenant_id,
        project_id=req.project,
        query=req.prompt,
        recent_messages=[],  # Could pass conversation history if available
    )

    # Use the formatted context as system instruction
    static_context_block = working_memory.context_text

    # 3. Retrieve episodic context from vector store
    try:
        embedding_service = get_embedding_service()
        query_embedding = embedding_service.generate_embeddings([req.prompt])[0]

        query_filters = {
            "must": [
                {"key": "tenant_id", "match": {"value": tenant_id}},
                {"key": "layer", "match": {"value": "em"}},
            ]
        }

        vector_store = get_vector_store(pool=request.app.state.pool)
        retrieved_items = await vector_store.query(
            query_embedding=query_embedding,
            top_k=50,
            filters=query_filters,
        )
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Error querying vector store: {e}"
        ) from e

    # ensure rerank_scores is always defined to avoid UnboundLocalError later
    rerank_scores = {}

    if not retrieved_items:
        final_items = []
        episodic_context_block = "No relevant episodic memories found."
    else:
        # Konwersja wyników Qdrant → format dla rerankera
        rerank_payload = {
            "query": req.prompt,
            "items": [
                {
                    "id": item.id,
                    "text": item.content,
                    "score": item.score,
                }
                for item in retrieved_items
            ],
        }

        # 4. Rerank
        try:
            async with httpx.AsyncClient() as client:
                rerank_resp = await client.post(
                    settings.RERANKER_API_URL + "/rerank",
                    json=rerank_payload,
                    timeout=60,
                )
                rerank_resp.raise_for_status()
                reranked_items = (await rerank_resp.json()).get("items", [])
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Reranker error: {e}")

        rerank_scores = {item["id"]: item["score"] for item in reranked_items}

        # 5. Wybór najlepszych 5
        final_items = sorted(
            [item for item in retrieved_items if item.id in rerank_scores],
            key=lambda x: rerank_scores[x.id],
            reverse=True,
        )[:5]
        episodic_context_block = "\n".join(
            [f"- {item.content}" for item in final_items]
        )

    # Update usage stats for the memories that were used
    used_memory_ids = [item.id for item in final_items]
    if used_memory_ids:
        await _update_memory_access_stats(
            memory_ids=used_memory_ids, tenant_id=tenant_id, pool=request.app.state.pool
        )

    # 6. LLM call – use static_context_block as system_instruction
    try:
        llm_provider = get_llm_provider()

        prompt_message = f"""
        EPISODIC CONTEXT (recent similar events):
        {episodic_context_block}

        CURRENT TASK:
        {req.prompt}
        """.strip()

        llm_result: LLMResult = await llm_provider.generate(
            system=static_context_block,
            prompt=prompt_message,
            model=settings.RAE_LLM_MODEL_DEFAULT,  # Use configured default model
        )
        answer = llm_result.text
        usage = llm_result.usage  # This is LLMResultUsage

        # Estimate token counts for cost_guard
        estimated_static_tokens = estimate_tokens(static_context_block)
        max(usage.prompt_tokens - estimated_static_tokens, 0)

        # Track cost and update budget
        cost_info = await track_request_cost(
            request=request,
            model_name=settings.RAE_LLM_MODEL_DEFAULT,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.candidates_tokens,
            tenant_id=tenant_id,
            project_id=req.project,
        )

        cost = CostInfo(
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.candidates_tokens,
            total_estimate=cost_info["total_cost_usd"] if cost_info else 0.0,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM call failed: {e}")

    # 7. Reflection hook
    try:
        reflection_content = f"User Query: {req.prompt}\n\nRetrieved Context:\n{episodic_context_block}\n\n---\n\nAgent Answer: {answer}"
        reflection_payload = StoreMemoryRequest(
            content=reflection_content,
            source=f"reflection_on_{llm_result.finish_reason}",
            layer="rm",
            tags=["reflection"],
        )

        async with httpx.AsyncClient() as client:
            headers = {"X-Tenant-Id": tenant_id, "X-API-Key": settings.API_KEY}
            await client.post(
                settings.MEMORY_API_URL + "/v1/memory/store",
                json=reflection_payload.dict(exclude_none=True),
                headers=headers,
            )

        reflection_event_counter.inc()  # Increment reflection event counter

    except Exception as e:
        # Log the error but don't fail the request
        print(f"Reflection hook failed: {e}")

    # Konwersja finalnych memories → ScoredMemoryRecord
    used_items = []
    for item in final_items:
        # The payload from qdrant should match the fields of MemoryRecord
        used_items.append(
            ScoredMemoryRecord(
                id=item.id,
                score=rerank_scores.get(item.id, item.score),
                content=item.content,
                source=item.source,
                importance=item.importance,
                layer=item.layer,
                tags=item.tags,
                timestamp=item.timestamp,
                last_accessed_at=item.last_accessed_at,
                usage_count=item.usage_count,
                project=item.project,
            )
        )

    used = QueryMemoryResponse(results=used_items)

    return AgentExecuteResponse(
        answer=answer,
        used_memories=used,
        cost=cost,
    )


async def _update_memory_access_stats(memory_ids: list[str], tenant_id: str, pool):
    """
    Updates the usage_count and last_accessed_at for a list of memories.

    This function is called after memories are retrieved and used in agent execution
    to track memory access patterns. These statistics are used by:
    - ImportanceScoringService for calculating memory importance
    - Memory decay mechanisms for identifying stale memories
    - Governance and analytics for usage tracking

    Args:
        memory_ids: List of memory IDs that were accessed
        tenant_id: Tenant identifier for security isolation
        pool: Database connection pool

    Notes:
        - Failures are logged but don't interrupt agent execution
        - Uses batch updates for performance
        - Updates are async and non-blocking
    """
    if not memory_ids:
        logger.debug("_update_memory_access_stats_skipped", reason="no_memory_ids")
        return

    try:
        from apps.memory_api.repositories.memory_repository import MemoryRepository

        repository = MemoryRepository(pool)
        updated_count = await repository.update_memory_access_stats(
            memory_ids=memory_ids, tenant_id=tenant_id
        )

        logger.debug(
            "_update_memory_access_stats_success",
            memory_count=len(memory_ids),
            updated_count=updated_count,
            tenant_id=tenant_id,
        )

    except Exception as e:
        # Log the error but don't fail the main request
        # Access stats are important but not critical for agent execution
        logger.error(
            "_update_memory_access_stats_failed",
            error=str(e),
            memory_count=len(memory_ids),
            tenant_id=tenant_id,
        )
