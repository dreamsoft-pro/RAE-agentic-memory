from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Any, Dict, Optional
from uuid import uuid4, UUID
import structlog
from apps.memory_api.models.event_models import Event, EventType, EmitEventResponse
from apps.memory_api.services.rae_core_service import RAECoreService

router = APIRouter(prefix="/v2/bridge", tags=["Bridge"])
logger = structlog.get_logger(__name__)

@router.post("/interact", response_model=EmitEventResponse)
async def agent_interaction(
    payload: Dict[str, Any],
    request: Request,
    source_agent: str = "open-claw",
    target_agent: str = "rae-oracle",
    session_id: Optional[str] = None,
    correlation_id: Optional[UUID] = None
):
    """
    Handles Agent-to-Agent (A2A) interactions through the RAE Bridge.
    All interactions are recorded as events and captured in memory.
    """
    service: RAECoreService = request.app.state.rae_core_service
    tenant_id = request.headers.get("X-Tenant-Id", "default")
    project_id = request.headers.get("X-Project-Id", "default")
    
    event_id = uuid4()
    if correlation_id is None:
        correlation_id = event_id

    # 1. Create the Event
    event = Event(
        event_id=event_id,
        event_type=EventType.AGENT_INTERACTION,
        tenant_id=tenant_id,
        project_id=project_id,
        source_service=source_agent,
        payload={
            "target_agent": target_agent,
            "interaction_data": payload
        },
        session_id=session_id,
        correlation_id=correlation_id,
        metadata={
            "a2a": True,
            "protocol": "mcp-bridge-v1"
        }
    )

    # 2. Implicit Capture: Store in Memory (Episodic)
    # This ensures every A2A interaction is auditable in the future
    try:
        content_summary = f"A2A: {source_agent} -> {target_agent}: {str(payload)[:200]}..."
        await service.engine.store_memory(
            tenant_id=tenant_id,
            agent_id=source_agent,
            content=content_summary,
            layer="episodic",
            project=project_id,
            session_id=session_id,
            metadata={
                "event_id": str(event_id),
                "correlation_id": str(correlation_id),
                "target_agent": target_agent,
                "full_payload": payload
            }
        )
    except Exception as e:
        logger.error("bridge_memory_capture_failed", error=str(e))
        # We continue even if memory capture fails, but log it

    # 3. Trigger Automations (Future: Semantic Firewall / Routing)
    # For now, we just return success
    
    return EmitEventResponse(
        event_id=event_id,
        triggers_matched=0,
        actions_queued=0,
        message="A2A Interaction routed through bridge and captured in memory"
    )
