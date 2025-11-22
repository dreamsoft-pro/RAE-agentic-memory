"""
ML Service - Microservice for Heavy ML Operations.

This service handles computationally expensive ML operations like:
- Entity resolution
- NLP processing
- Advanced embeddings

This separation keeps the main memory API lightweight and fast.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import structlog

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="RAE ML Service",
    description="Machine Learning microservice for RAE - handles entity resolution and NLP",
    version="2.0.0"
)


# --- Models ---

class EntityResolutionRequest(BaseModel):
    """Request model for entity resolution."""
    nodes: List[Dict[str, Any]]
    similarity_threshold: float = 0.85


class EntityResolutionResponse(BaseModel):
    """Response model for entity resolution."""
    merge_groups: List[List[str]]
    statistics: Dict[str, Any]


class ExtractTriplesRequest(BaseModel):
    """Request model for triple extraction."""
    text: str
    language: str = "en"


class ExtractTriplesResponse(BaseModel):
    """Response model for triple extraction."""
    triples: List[Dict[str, str]]


# --- Endpoints ---

@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "RAE ML Service",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "resolve_entities": "/resolve-entities",
            "extract_triples": "/extract-triples"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ml-service"}


@app.post("/resolve-entities", response_model=EntityResolutionResponse)
async def resolve_entities(req: EntityResolutionRequest):
    """
    Resolve duplicate entities using ML similarity matching.

    Uses sentence transformers and agglomerative clustering to identify
    groups of similar entities that should potentially be merged.
    """
    logger.info(
        "entity_resolution_requested",
        node_count=len(req.nodes),
        threshold=req.similarity_threshold
    )

    try:
        # Import here to avoid loading ML models at startup
        from apps.ml_service.services.entity_resolution import EntityResolutionMLService

        # Initialize service
        resolution_service = EntityResolutionMLService(
            similarity_threshold=req.similarity_threshold
        )

        # Perform entity resolution
        merge_groups, statistics = resolution_service.resolve_entities(
            nodes=req.nodes,
            similarity_threshold=req.similarity_threshold
        )

        return EntityResolutionResponse(
            merge_groups=merge_groups,
            statistics=statistics
        )

    except Exception as e:
        logger.exception("entity_resolution_failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Entity resolution failed: {str(e)}"
        )


@app.post("/extract-triples", response_model=ExtractTriplesResponse)
async def extract_triples(req: ExtractTriplesRequest):
    """
    Extract knowledge triples from text using NLP.

    This endpoint will be implemented in Faza 2.2.
    """
    logger.info(
        "triple_extraction_requested",
        text_length=len(req.text),
        language=req.language
    )

    # Placeholder implementation
    # TODO: Implement actual triple extraction in Faza 2.2
    return ExtractTriplesResponse(
        triples=[]
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
