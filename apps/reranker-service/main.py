from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Reranker Service", version="0.1")

class RerankItem(BaseModel):
    id: str
    text: str
    score: float | None = None

class RerankRequest(BaseModel):
    query: str
    items: List[RerankItem]

class RerankResponse(BaseModel):
    items: List[RerankItem]

@app.post("/rerank", response_model=RerankResponse)
def rerank(req: RerankRequest):
    # v1: sortowanie po score lub identity
    sorted_items = sorted(req.items, key=lambda x: x.score if x.score is not None else 0, reverse=True)
    return RerankResponse(items=sorted_items)
