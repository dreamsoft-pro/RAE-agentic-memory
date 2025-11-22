"""
ML Service - Microservice for Heavy ML Operations.

This service handles computationally expensive ML operations like:
- Entity resolution
- NLP processing
- Advanced embeddings

This separation keeps the main memory API lightweight and fast.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import structlog

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="RAE ML Service",
    description="Machine Learning microservice for RAE - handles entity resolution, embeddings, and NLP",
    version="2.0.0"
)


# --- Models ---

class EmbeddingRequest(BaseModel):
    """Request model for generating embeddings."""
    texts: List[str] = Field(..., description="List of texts to embed")
    model: str = Field(default="all-MiniLM-L6-v2", description="Name of the embedding model to use")


class EmbeddingResponse(BaseModel):
    """Response model for embeddings."""
    embeddings: List[List[float]] = Field(..., description="List of embedding vectors")
    model: str = Field(..., description="Model used for embeddings")
    dimension: int = Field(..., description="Dimension of embedding vectors")


class EntityResolutionRequest(BaseModel):
    """Request model for entity resolution."""
    nodes: List[Dict[str, Any]]
    similarity_threshold: float = 0.85


class EntityResolutionResponse(BaseModel):
    """Response model for entity resolution."""
    merge_groups: List[List[str]]
    statistics: Dict[str, Any]


class ExtractKeywordsRequest(BaseModel):
    """Request model for keyword extraction."""
    text: str = Field(..., description="Text to extract keywords from")
    max_keywords: int = Field(default=10, ge=1, le=50, description="Maximum number of keywords to return")
    language: str = Field(default="en", description="Language code")


class ExtractKeywordsResponse(BaseModel):
    """Response model for keyword extraction."""
    keywords: List[Dict[str, Any]] = Field(..., description="List of extracted keywords with metadata")


class ExtractTriplesRequest(BaseModel):
    """Request model for triple extraction."""
    text: str = Field(..., description="Text to extract triples from")
    language: str = Field(default="en", description="Language code")
    method: str = Field(default="dependency", description="Extraction method: 'dependency' or 'simple'")


class ExtractTriplesResponse(BaseModel):
    """Response model for triple extraction."""
    triples: List[Dict[str, str]] = Field(..., description="List of extracted knowledge triples")


# --- Endpoints ---

@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "RAE ML Service",
        "version": "2.0.0",
        "status": "operational",
        "description": "Microservice handling heavy ML operations for RAE",
        "endpoints": {
            "health": "/health",
            "embeddings": "/embeddings",
            "resolve_entities": "/resolve-entities",
            "extract_keywords": "/extract-keywords",
            "extract_triples": "/extract-triples"
        },
        "features": [
            "Local embedding generation (SentenceTransformers)",
            "Entity resolution and clustering",
            "Keyword extraction (spaCy)",
            "Knowledge triple extraction",
            "NLP processing"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ml-service"}


@app.post("/embeddings", response_model=EmbeddingResponse)
async def generate_embeddings(req: EmbeddingRequest):
    """
    Generate embeddings for texts using local SentenceTransformer models.

    This endpoint provides fast, local embedding generation without
    relying on external APIs. Perfect for high-throughput scenarios.

    Example request:
    ```json
    {
        "texts": ["Hello world", "AI is awesome"],
        "model": "all-MiniLM-L6-v2"
    }
    ```
    """
    logger.info(
        "embedding_generation_requested",
        text_count=len(req.texts),
        model=req.model
    )

    try:
        # Import here to avoid loading models at startup
        from apps.ml_service.services.embedding_service import EmbeddingMLService

        # Initialize service (singleton)
        embedding_service = EmbeddingMLService(model_name=req.model)

        # Generate embeddings
        embeddings = embedding_service.generate_embeddings(req.texts)

        return EmbeddingResponse(
            embeddings=embeddings,
            model=req.model,
            dimension=embedding_service.get_embedding_dimension()
        )

    except Exception as e:
        logger.exception("embedding_generation_failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Embedding generation failed: {str(e)}"
        )


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


@app.post("/extract-keywords", response_model=ExtractKeywordsResponse)
async def extract_keywords(req: ExtractKeywordsRequest):
    """
    Extract keywords and key phrases from text using spaCy NLP.

    Identifies important terms including:
    - Named entities (people, places, organizations)
    - Noun phrases
    - Key terms (nouns, proper nouns, adjectives)

    Example request:
    ```json
    {
        "text": "Apple Inc. announced new AI features in California",
        "max_keywords": 10,
        "language": "en"
    }
    ```
    """
    logger.info(
        "keyword_extraction_requested",
        text_length=len(req.text),
        max_keywords=req.max_keywords,
        language=req.language
    )

    try:
        # Import here to avoid loading models at startup
        from apps.ml_service.services.nlp_service import NLPService

        # Initialize service (singleton)
        nlp_service = NLPService(language=req.language)

        # Extract keywords
        keywords = nlp_service.extract_keywords(
            text=req.text,
            max_keywords=req.max_keywords,
            language=req.language
        )

        return ExtractKeywordsResponse(
            keywords=keywords
        )

    except Exception as e:
        logger.exception("keyword_extraction_failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Keyword extraction failed: {str(e)}"
        )


@app.post("/extract-triples", response_model=ExtractTriplesResponse)
async def extract_triples(req: ExtractTriplesRequest):
    """
    Extract knowledge triples from text using dependency parsing.

    Extracts structured (subject, predicate, object) triples representing
    relationships and facts mentioned in the text.

    Supports two methods:
    - **dependency**: Full dependency parsing (more accurate)
    - **simple**: Pattern-based extraction (faster)

    Example request:
    ```json
    {
        "text": "Albert Einstein developed the theory of relativity",
        "language": "en",
        "method": "dependency"
    }
    ```

    Example response:
    ```json
    {
        "triples": [
            {
                "subject": "Albert Einstein",
                "predicate": "develop",
                "object": "the theory of relativity",
                "confidence": 0.8
            }
        ]
    }
    ```
    """
    logger.info(
        "triple_extraction_requested",
        text_length=len(req.text),
        language=req.language,
        method=req.method
    )

    try:
        # Import here to avoid loading models at startup
        from apps.ml_service.services.triple_extraction import TripleExtractionService

        # Initialize service (singleton)
        triple_service = TripleExtractionService(language=req.language)

        # Extract triples using selected method
        if req.method == "simple":
            triples = triple_service.extract_simple_triples(req.text)
        else:
            triples = triple_service.extract_triples(req.text, language=req.language)

        logger.info(
            "triple_extraction_completed",
            triple_count=len(triples),
            method=req.method
        )

        return ExtractTriplesResponse(
            triples=triples
        )

    except Exception as e:
        logger.exception("triple_extraction_failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Triple extraction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
