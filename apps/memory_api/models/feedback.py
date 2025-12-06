from typing import Optional

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    memory_id: str = Field(..., description="ID of the memory to provide feedback on")
    feedback_type: str = Field(
        ..., pattern="^(positive|negative)$", description="Type of feedback"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    context_id: Optional[str] = Field(
        None, description="Context/Trace ID where memory was used"
    )
