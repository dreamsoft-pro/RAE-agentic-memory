import structlog
from fastapi import APIRouter, Depends, Request

from apps.memory_api.models.feedback import FeedbackRequest
from apps.memory_api.repositories.memory_repository import MemoryRepository
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services.feedback_service import FeedbackService

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=dict)
async def submit_feedback(
    feedback: FeedbackRequest,
    request: Request,
    tenant_id: str = Depends(get_and_verify_tenant_id),
):
    """
    Submit feedback for a retrieved memory.

    Used for the 'Feedback Loop' mechanism to adjust memory importance.
    """
    # Initialize service (in production, use dependency injection properly)
    pool = request.app.state.pool
    repo = MemoryRepository(pool)
    service = FeedbackService(repo)

    success = await service.process_feedback(
        tenant_id=tenant_id,
        memory_id=feedback.memory_id,
        feedback_type=feedback.feedback_type,
        comment=feedback.comment,
    )

    if not success:
        # Could be disabled feature or memory not found
        # For API UX, we return 200 OK but with status
        return {"status": "ignored_or_failed", "message": "Feedback not applied"}

    return {"status": "success", "message": "Feedback recorded"}
