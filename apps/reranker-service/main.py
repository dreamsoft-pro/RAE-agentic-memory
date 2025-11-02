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
    # STUB: zwróć w tej samej kolejności; implementacja modelu do uzupełnienia
    return RerankResponse(items=req.items)
