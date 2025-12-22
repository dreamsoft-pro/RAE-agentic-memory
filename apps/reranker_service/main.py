from typing import List

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sentence_transformers import CrossEncoder

app = FastAPI(title="Reranker Service", version="0.1")
Instrumentator().instrument(app).expose(app)

# Load the cross-encoder model at startup
# This model is lightweight and effective for semantic search.
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


class RerankItem(BaseModel):
    id: str
    text: str
    score: float | None = None


class RerankRequest(BaseModel):
    query: str
    items: List[RerankItem]


class RerankResponse(BaseModel):
    items: List[RerankItem]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/rerank", response_model=RerankResponse)
def rerank(req: RerankRequest):
    """
    Reranks the provided items based on their relevance to the query using a cross-encoder model.
    """
    if not req.items:
        return RerankResponse(items=[])

    # Create pairs of [query, item_text] for the model
    model_input = [[req.query, item.text] for item in req.items]

    # Predict the scores
    scores = model.predict(model_input)

    # Assign the new scores to the items
    for item, score in zip(req.items, scores):
        item.score = float(score)

    # Sort items by the new score in descending order
    sorted_items = sorted(req.items, key=lambda x: x.score or 0.0, reverse=True)

    return RerankResponse(items=sorted_items)
