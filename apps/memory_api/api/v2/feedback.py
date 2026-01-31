"""
Feedback API v2 - powered by RAE-Core.
"""

from typing import Any, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from apps.memory_api.dependencies import get_rae_core_service
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services.feedback_service import FeedbackService
from apps.memory_api.services.rae_core_service import RAECoreService

router = APIRouter(prefix="/v2/feedback", tags=["Feedback v2 (RAE-Core)"])
logger = structlog.get_logger(__name__)


class FeedbackRequestV2(BaseModel):
    memory_id: str
    feedback_type: str = Field(..., pattern="^(positive|negative)$")
    score: float = Field(..., ge=0.0, le=1.0)
    comment: Optional[str] = None
    query_text: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.post("/", response_model=dict)
async def submit_feedback(
    request: FeedbackRequestV2,
    tenant_id: UUID = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    Submit feedback for a retrieved memory.
    """
    service = FeedbackService(rae_service=rae_service)

    success = await service.process_feedback(
        tenant_id=str(tenant_id),
        memory_id=request.memory_id,
        feedback_type=request.feedback_type,
        comment=request.comment,
        score=request.score,
        query_text=request.query_text,
        metadata=request.metadata,
    )

    if not success:
        return {"status": "ignored_or_failed", "message": "Feedback not applied"}

    return {"status": "success", "message": "Feedback recorded"}
