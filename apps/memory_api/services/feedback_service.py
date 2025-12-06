"""
Feedback Service (Iteration 3)

Implements the "Feedback Loop" (learning-to-remember) mechanism.
"""

from typing import Optional

import structlog

from apps.memory_api.config import settings
from apps.memory_api.repositories.memory_repository import MemoryRepository

logger = structlog.get_logger(__name__)


class FeedbackService:
    """
    Service for processing user/system feedback on memory retrieval quality.
    """

    def __init__(self, memory_repo: MemoryRepository):
        self.memory_repo = memory_repo

    async def process_feedback(
        self,
        tenant_id: str,
        memory_id: str,
        feedback_type: str,
        comment: Optional[str] = None,
    ) -> bool:
        """
        Process feedback for a specific memory.

        Args:
            tenant_id: Tenant ID.
            memory_id: ID of the memory.
            feedback_type: "positive" or "negative".
            comment: Optional text comment.

        Returns:
            True if updated successfully.
        """
        if not settings.ENABLE_FEEDBACK_LOOP:
            logger.info("feedback_loop_disabled")
            return False

        delta = 0.0
        if feedback_type == "positive":
            delta = settings.FEEDBACK_POSITIVE_DELTA
        elif feedback_type == "negative":
            delta = -settings.FEEDBACK_NEGATIVE_DELTA
        else:
            logger.warning("invalid_feedback_type", type=feedback_type)
            return False

        new_score = await self.memory_repo.update_importance(
            memory_id=memory_id, tenant_id=tenant_id, delta=delta
        )

        if new_score is not None:
            logger.info(
                "feedback_processed",
                memory_id=memory_id,
                type=feedback_type,
                delta=delta,
                new_score=new_score,
            )
            return True

        return False
