"""
RAE-Lite Local HTTP Server.

FastAPI server running locally for RAE-Lite.
"""

import os
from pathlib import Path

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rae_adapters.sqlite import (
    SQLiteGraphStore,
    SQLiteStorage,
    SQLiteVectorStore,
)
from rae_core.config.settings import RAESettings
from rae_core.embedding.native import NativeEmbeddingProvider
from rae_core.engine import RAEEngine
from rae_core.interfaces.embedding import IEmbeddingProvider
from rae_lite.config import settings

logger = structlog.get_logger(__name__)

# SYSTEM 22.3: Production-ready embedding logic for RAE-Lite
project_root = Path(os.environ.get("PROJECT_ROOT", os.getcwd()))
model_dir = project_root / "models" / "nomic-embed-text-v1.5"
model_path = model_dir / "model.onnx"
tokenizer_path = model_dir / "tokenizer.json"

if model_path.exists() and tokenizer_path.exists():
    logger.info("using_native_embeddings", path=str(model_path))
    embedding_provider = NativeEmbeddingProvider(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        model_name="nomic-embed-text-v1.5"
    )
else:
    logger.warning("native_models_missing_using_mock", path=str(model_path))
    class LocalEmbeddingProvider(IEmbeddingProvider):
        def __init__(self):
            self.dimension = 384
        async def embed_text(self, text: str, task_type: str = "search_document") -> list[float]:
            val = (len(text) % 100) / 100.0
            return [val] * self.dimension
        async def embed_batch(self, texts: list[str], task_type: str = "search_document") -> list[list[float]]:
            return [await self.embed_text(t, task_type) for t in texts]
        def get_dimension(self) -> int:
            return self.dimension
    embedding_provider = LocalEmbeddingProvider()

# Initialize SQLite adapters
memory_storage = SQLiteStorage(str(settings.db_path))
vector_store = SQLiteVectorStore(str(settings.vector_db_path))
graph_store = SQLiteGraphStore(str(settings.graph_db_path))

# Configure RAE Core Settings
rae_settings = RAESettings()
rae_settings.sensory_max_size = 50
rae_settings.working_max_size = 50
rae_settings.vector_backend = "sqlite"
rae_settings.vector_dimension = embedding_provider.get_dimension()

# Initialize RAE Engine
engine = RAEEngine(
    memory_storage=memory_storage,
    vector_store=vector_store,
    embedding_provider=embedding_provider,
    settings=rae_settings,
)

# FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Local-first AI Memory Desktop App",
)

# CORS - allow all for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class StoreMemoryRequest(BaseModel):
    """Store memory request."""

    content: str = Field(..., min_length=1)
    source: str = Field(default="rae-lite")
    project: str = Field(default="default")
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)


class QueryMemoryRequest(BaseModel):
    """Query memory request."""

    query: str = Field(..., min_length=1)
    project: str = Field(default="default")
    k: int = Field(default=10, gt=0, le=100)
    layers: list[str] | None = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


@app.post("/memories")
async def store_memory(request: StoreMemoryRequest):
    """Store a memory."""
    try:
        # Store in engine (which handles both volatile and persistent layers)
        memory_id = await engine.store_memory(
            content=request.content,
            source=request.source,
            importance=request.importance,
            tags=request.tags,
            tenant_id="local",
            agent_id="rae-lite-user",
            project=request.project,
        )

        return {"memory_id": str(memory_id), "status": "stored"}

    except Exception as e:
        logger.error("store_memory_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memories/query")
async def query_memories(request: QueryMemoryRequest):
    """Query memories."""
    try:
        response = await engine.query_memory(
            query=request.query,
            k=request.k,
            filters={"project": request.project},
            search_layers=request.layers,
        )

        return {
            "results": [
                {
                    "id": r.id,
                    "content": r.content,
                    "score": r.score,
                    "layer": r.layer,
                    "importance": r.importance,
                    "tags": r.tags or [],
                }
                for r in response.results
            ],
            "total": len(response.results),
            "synthesized_context": response.synthesized_context,
        }

    except Exception as e:
        logger.error("query_memories_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/statistics")
async def get_statistics():
    """Get memory statistics."""
    try:
        stats = await engine.get_statistics()
        return stats
    except Exception as e:
        logger.error("get_statistics_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/consolidate")
async def consolidate():
    """Trigger memory consolidation."""
    try:
        results = await engine.consolidate_memories(
            tenant_id="local", project="default"
        )
        return {"status": "completed", "results": results}
    except Exception as e:
        logger.error("consolidate_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reflections")
async def generate_reflections():
    """Generate reflections."""
    try:
        reflections = await engine.generate_reflections(
            tenant_id="local", project="default"
        )
        return {
            "status": "completed",
            "count": len(reflections),
            "reflections": [
                {
                    "id": r.id,
                    "content": r.content,
                    "importance": r.importance,
                    "tags": r.tags or [],
                }
                for r in reflections
            ],
        }
    except Exception as e:
        logger.error("generate_reflections_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
