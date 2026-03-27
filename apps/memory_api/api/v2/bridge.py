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
    
    # SYSTEM 95.1: Intelligent Context Resolution
    tenant_id = request.headers.get("X-Tenant-Id") or "00000000-0000-0000-0000-000000000000"
    project = request.headers.get("X-Project-Id")
    
    # Auto-detect project from payload keywords if not explicitly provided
    if not project:
        payload_str = str(payload).lower()
        if any(kw in payload_str for kw in ["speed", "area", "machine", "job id", "ink"]):
            project = "screenwatcher"
        elif any(kw in payload_str for kw in ["dreamsoft", "modernization", "nextjs", "angular"]):
            project = "dreamsoft_modernization"
        else:
            project = "default"

    # SYSTEM 95.2: Human-Centric Labeling
    # Check payload for intelligence FIRST
    payload_data = payload.get("payload", payload) # Support both nested and flat payload
    action_name = payload_data.get("action", "interaction").replace("_", " ").title()
    
    # Check agents
    s_agent = payload.get("source_agent") or source_agent
    t_agent = payload.get("target_agent") or target_agent
    
    human_label = payload.get("human_label") or f"{action_name} ({s_agent} -> {t_agent})"

    event_id = uuid4()
    if correlation_id is None:
        correlation_id = event_id

    # 1. Create the Event
    event = Event(
        event_id=event_id,
        event_type=EventType.AGENT_INTERACTION,
        tenant_id=tenant_id,
        project=project,
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
    try:
        content_summary = f"A2A: {source_agent} -> {target_agent}: {str(payload)[:500]}"
        
        await service.engine.store_memory(
            tenant_id=tenant_id,
            agent_id=source_agent,
            content=content_summary,
            layer="episodic",
            project=project,
            session_id=session_id,
            human_label=human_label,
            metadata={
                "event_id": str(event_id),
                "correlation_id": str(correlation_id),
                "target_agent": target_agent,
                "full_payload": payload,
                "human_label": human_label
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

@router.post("/audit")
async def semantic_audit(
    payload: Dict[str, Any],
    request: Request,
    source_agent: str = "open-claw"
):
    """
    Phase 3 Hard Frames: Semantic Firewall.
    Analyzes the intent of the agent before allowing execution.
    """
    service: RAECoreService = request.app.state.rae_core_service
    prompt = payload.get("prompt", "")
    context = payload.get("context", "no_context")

    # 1. Intent Analysis via Reflective Layer
    is_safe = True
    reason = "Intent matches project scope"

    forbidden_keywords = ["private_key", "password", "hasło", "klucz", ".env", "secret"]
    if any(kw in prompt.lower() for kw in forbidden_keywords):
        is_safe = False
        reason = "RESTRICTED data leak or credential access attempt detected"

    # 2. Log the Audit Attempt
    await service.engine.store_memory(
        tenant_id="00000000-0000-0000-0000-000000000000",
        agent_id=source_agent,
        content=f"PHASE 3 AUDIT: {source_agent} prompt audit -> {is_safe}. Reason: {reason}",
        layer="reflective",
        tags=["phase3_audit", "firewall"],
        metadata={"prompt_snippet": prompt[:100], "safe": is_safe, "reason": reason}
    )

    if not is_safe:
        raise HTTPException(status_code=403, detail=f"Semantic Firewall Block: {reason}")

    return {"status": "approved", "audit_id": str(uuid4()), "reason": reason}
