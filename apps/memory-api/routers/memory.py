from fastapi import APIRouter, Depends, Request
from . import deps  # placeholder jeśli chcesz dodać zależności
from ..models import AddMemoryRequest, AddMemoryResponse, QueryRequest, QueryResponse, QueryResultItem, MemoryType
from ..services import qdrant_client

router = APIRouter(prefix="/memory", tags=["memory"])

@router.post("/add", response_model=AddMemoryResponse)
async def add_memory(req: AddMemoryRequest, request: Request):
    # PII scrub + zapis do Postgresa (memories + specialized) — TODO
    memory_id = qdrant_client.add_memory_vectorized(req.dict())
    return AddMemoryResponse(memory_id=memory_id)

@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest, request: Request):
    # Hybrydowe wyszukiwanie z Qdrant + rerank — TODO
    items = []
    return QueryResponse(results=items)
