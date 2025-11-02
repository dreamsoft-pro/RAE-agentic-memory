from fastapi import APIRouter, Request
from ..models import AgentExecuteRequest, AgentExecuteResponse, QueryResponse, CostInfo
from ..middleware.cost_guard import cost_guard

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/execute", response_model=AgentExecuteResponse)
@cost_guard()
async def execute(req: AgentExecuteRequest, request: Request):
    # TODO: retrieve → rerank → build prompt → call LLM (Gemini) via factory
    used = QueryResponse(results=[])
    cost = CostInfo(input_tokens=0, output_tokens=0, total_estimate=0.0)
    return AgentExecuteResponse(answer="(stub)", used_memories=used, cost=cost)
