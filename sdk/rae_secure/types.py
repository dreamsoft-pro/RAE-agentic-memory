from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AgentIntent(BaseModel):
    """
    The Agent declares WHAT it wants to do, not HOW.
    Examples: "summarize_text", "extract_entities", "generate_code"
    """
    name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: str = "normal"

class MemoryContext(BaseModel):
    """
    Context provided by the Kernel to the Agent.
    The Agent does not query the DB directly.
    """
    session_id: str
    relevant_memories: List[str] # Content of memories
    metadata: Dict[str, Any] = Field(default_factory=dict)

class KernelResponse(BaseModel):
    """
    Response from the RAE Kernel.
    """
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    cost_tokens: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
