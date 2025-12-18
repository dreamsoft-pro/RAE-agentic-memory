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
from apps.memory_api.observability.rae_tracing import get_tracer
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
tracer = get_tracer(__name__)


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

    with tracer.start_as_current_span("rae.api.agent.execute") as span:
        span.set_attribute("rae.tenant_id", tenant_id)
        span.set_attribute("rae.project_id", req.project)
        span.set_attribute("rae.agent.prompt_length", len(req.prompt))
        span.set_attribute("rae.agent.model", settings.RAE_LLM_MODEL_DEFAULT)

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
        span.set_attribute("rae.agent.context_tokens", working_memory.total_tokens)
        span.set_attribute(
            "rae.agent.reflections_count", len(working_memory.reflections)
        )

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
            span.set_attribute("rae.agent.retrieved_items_count", len(retrieved_items))
        except Exception as e:
            span.set_attribute("rae.outcome.label", "vector_store_error")
            span.set_attribute("rae.error.message", str(e))
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
                span.set_attribute(
                    "rae.agent.reranked_items_count", len(reranked_items)
                )
            except Exception as e:
                span.set_attribute("rae.outcome.label", "reranker_error")
                span.set_attribute("rae.error.message", str(e))
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
            span.set_attribute("rae.agent.final_items_count", len(final_items))

        # Update usage stats for the memories that were used
        used_memory_ids = [item.id for item in final_items]
        if used_memory_ids:
            try:
                # Use RAECoreService to update stats
                from apps.memory_api.dependencies import get_rae_core_service
                rae_service = get_rae_core_service(request)
                await rae_service.update_memory_access_batch(
                    memory_ids=used_memory_ids,
                    tenant_id=tenant_id
                )
            except Exception as e:
                # Log error but don't fail request
                logger.error("update_memory_stats_failed", error=str(e))

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

            # Add telemetry for LLM call
            span.set_attribute("rae.agent.llm_input_tokens", usage.prompt_tokens)
            span.set_attribute("rae.agent.llm_output_tokens", usage.candidates_tokens)
            span.set_attribute("rae.agent.llm_total_cost_usd", cost.total_estimate)
            span.set_attribute("rae.agent.llm_finish_reason", llm_result.finish_reason)

        except Exception as e:
            span.set_attribute("rae.outcome.label", "llm_error")
            span.set_attribute("rae.error.message", str(e))
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
                    json=reflection_payload.model_dump(exclude_none=True),
                    headers=headers,
                )

            reflection_event_counter.inc()  # Increment reflection event counter
            span.set_attribute("rae.agent.reflection_stored", True)

        except Exception as e:
            # Log the error but don't fail the request
            span.set_attribute("rae.agent.reflection_stored", False)
            span.set_attribute("rae.agent.reflection_error", str(e))
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

        span.set_attribute("rae.agent.used_memories_count", len(used_items))
        span.set_attribute("rae.outcome.label", "success")

        return AgentExecuteResponse(
            answer=answer,
            used_memories=used,
            cost=cost,
        )
