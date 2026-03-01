"""
Agent API v2 - powered by RAE-Core.
"""

from typing import Any
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from apps.memory_api.dependencies import get_rae_core_service
from apps.memory_api.observability.rae_tracing import get_tracer
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services.rae_core_service import RAECoreService

router = APIRouter(prefix="/v2/agent", tags=["Agent v2 (RAE-Core)"])
logger = structlog.get_logger(__name__)
tracer = get_tracer(__name__)


class AgentExecuteRequestV2(BaseModel):
    prompt: str = Field(..., min_length=1)
    project: str = Field(..., min_length=1)
    session_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentExecuteResponseV2(BaseModel):
    answer: str
    session_id: str | None = None
    cost_estimate: float = 0.0


@router.post("/execute", response_model=AgentExecuteResponseV2)
async def execute_agent(
    request: AgentExecuteRequestV2,
    http_request: Request,
    tenant_id: UUID = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    Execute agent reasoning using RAE-Core Runtime.
    """
    with tracer.start_as_current_span("rae.api.v2.agent.execute") as span:
        span.set_attribute("rae.tenant_id", str(tenant_id))
        span.set_attribute("rae.project", request.project)

        try:
            action = await rae_service.execute_action(
                tenant_id=tenant_id,
                agent_id=request.project,
                prompt=request.prompt,
                session_id=request.session_id,
                metadata=request.metadata,
            )

            return AgentExecuteResponseV2(
                answer=str(action.content),
                session_id=request.session_id,
                cost_estimate=0.0,  # TODO: Real cost from Action object
            )
        except Exception as e:
            logger.error("agent_execute_failed", error=str(e), tenant_id=tenant_id)
            raise HTTPException(status_code=500, detail=str(e))
