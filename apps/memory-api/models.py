from typing import List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class MemoryType(str, Enum):
    episodic = "episodic"
    semantic = "semantic"
    procedural = "procedural"

class AddMemoryRequest(BaseModel):
    tenant_id: str
    agent_id: str
    memory_type: MemoryType
    content: str
    source_id: Optional[str] = None
    created_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None

class AddMemoryResponse(BaseModel):
    memory_id: str

class QueryFilters(BaseModel):
    memory_type: Optional[MemoryType] = None
    min_saliency: Optional[float] = None
    since: Optional[datetime] = None

class QueryRequest(BaseModel):
    tenant_id: str
    query_text: str
    k: int = 50
    k_final: int = 5
    filters: Optional[QueryFilters] = None

class QueryResultItem(BaseModel):
    memory_id: str
    score: float
    content: str
    source_id: Optional[str] = None
    memory_type: MemoryType
    provenance: Optional[dict[str, Any]] = None

class QueryResponse(BaseModel):
    results: List[QueryResultItem] = []

class AgentExecuteRequest(BaseModel):
    tenant_id: str
    prompt: str
    tools_allowed: Optional[List[str]] = None
    budget_tokens: int = 20000

class CostInfo(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_estimate: float = 0.0

class AgentExecuteResponse(BaseModel):
    answer: str
    used_memories: QueryResponse
    cost: CostInfo

class TimelineItem(BaseModel):
    memory_id: str
    created_at: datetime
    content: str
    memory_type: MemoryType
    saliency_score: float

class TimelineResponse(BaseModel):
    items: List[TimelineItem] = []
