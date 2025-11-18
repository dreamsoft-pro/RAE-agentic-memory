import os
import psycopg2
from fastapi import APIRouter, Depends, Request
from . import deps
from ..models import AddMemoryRequest, AddMemoryResponse, QueryRequest, QueryResponse, QueryResultItem, MemoryType, TimelineResponse, TimelineItem
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

def _get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        dbname=os.environ.get("POSTGRES_DB", "memory"),
        user=os.environ.get("POSTGRES_USER", "memory"),
        password=os.environ.get("POSTGRES_PASSWORD", "example")
    )

@router.get("/timeline", response_model=TimelineResponse)
async def timeline(request: Request):
    tenant_id = request.headers.get("X-Tenant-Id")
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SET app.tenant_id = %s", (tenant_id,))
    cursor.execute("SELECT memory_id, created_at, content, memory_type, saliency_score FROM memories ORDER BY created_at DESC LIMIT 100")
    items = [TimelineItem(memory_id=row[0], created_at=row[1], content=row[2], memory_type=row[3], saliency_score=row[4]) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return TimelineResponse(items=items)
