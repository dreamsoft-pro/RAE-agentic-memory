import requests, os, json
from fastapi import APIRouter, Request
from ..models import AgentExecuteRequest, AgentExecuteResponse, QueryResponse, CostInfo, QueryRequest, QueryResultItem
from ..middleware.cost_guard import cost_guard
from ..services import qdrant_client

router = APIRouter(prefix="/agent", tags=["agent"])

def _reranker_url() -> str:
    return os.environ.get("RERANKER_API_URL", "http://localhost:8001")

@router.post("/execute", response_model=AgentExecuteResponse)
@cost_guard()
async def execute(req: AgentExecuteRequest, request: Request):
    # 1. Retrieve
    retrieved_items = qdrant_client.hybrid_search(req.prompt, k=50, filters={"tenant_id": req.tenant_id})

    # 2. Rerank
    rerank_req = {
        "query": req.prompt,
        "items": [{"id": item['id'], "text": item['text'], "score": item['score']} for item in retrieved_items]
    }
    rerank_resp = requests.post(f"{_reranker_url()}/rerank", json=rerank_req)
    rerank_resp.raise_for_status()
    reranked_ids = {item['id']: item['score'] for item in rerank_resp.json()['items']}

    # 3. Build prompt (stub)
    final_items = sorted([item for item in retrieved_items if item['id'] in reranked_ids], key=lambda x: reranked_ids[x['id']], reverse=True)[:5]

    # 3. Build prompt
    prompt_context = "\n".join([item['text'] for item in final_items])
    final_prompt = f"Context:\n{prompt_context}\n\nUser query: {req.prompt}"

    # 4. Call LLM (stub - returning the prompt for now)
    answer = f"LLM prompt would be: {final_prompt}"

    used = QueryResponse(results=[QueryResultItem(**item) for item in final_items])
    cost = CostInfo(input_tokens=len(final_prompt.split()), output_tokens=len(answer.split()), total_estimate=0.0)
    return AgentExecuteResponse(answer=answer, used_memories=used, cost=cost)
