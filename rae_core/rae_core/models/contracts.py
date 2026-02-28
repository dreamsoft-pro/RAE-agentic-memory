from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class AgentDecision(str, Enum):
    PROCEED = "proceed"
    RETRY = "retry"
    ABORT = "abort"
    INSUFFICIENT_DATA = "insufficient_data"
    ESCALATE = "escalate"

class AgentOutputContract(BaseModel):
    """
    Enhanced Contract: Full Decision Provenance.
    Ensures that every decision is linked to specific evidence.
    """
    analysis: str = Field(..., min_length=10, description="Deep reasoning behind the decision")
    decision: AgentDecision = Field(..., description="Selected action")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    
    # REQUIRED: Explicit list of source memory IDs that justify this decision
    retrieved_sources: List[str] = Field(..., min_length=1, description="IDs of memories used as evidence")
    
    # OPTIONAL: Metadata about the model and pattern
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('retrieved_sources')
    @classmethod
    def must_have_evidence(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Decision must be grounded in at least one source memory.")
        return v

class ContractValidationResult(BaseModel):
    is_valid: bool = False
    block_reasons: List[str] = Field(default_factory=list)
    audit_trace_id: Optional[str] = None
