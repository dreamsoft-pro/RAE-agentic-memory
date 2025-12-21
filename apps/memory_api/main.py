from contextlib import asynccontextmanager
from typing import Any, cast

import asyncpg
import structlog
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi.errors import RateLimitExceeded

from apps.memory_api.api.v1 import (
    agent,
    cache,
    compliance,
    feedback,
    governance,
    graph,
    memory,
)
from apps.memory_api.config import settings
from apps.memory_api.dependencies import create_redis_client
from apps.memory_api.logging_config import setup_logging
from apps.memory_api.middleware.budget_enforcer import BudgetEnforcementMiddleware
from apps.memory_api.middleware.rate_limiter import limiter, rate_limit_exceeded_handler
from apps.memory_api.middleware.tenant import TenantContextMiddleware
from apps.memory_api.observability import health_checks as health_router
from apps.memory_api.observability import (
    instrument_fastapi,
    instrument_libraries,
    setup_opentelemetry,
)
from apps.memory_api.routes import (
    dashboard,
    evaluation,
    event_triggers,
    graph_enhanced,
    hybrid_search,
    reflections,
    token_savings,
)
from apps.memory_api.security import auth
from apps.memory_api.security.rate_limit import rate_limit_middleware
from apps.memory_api.services.context_cache import rebuild_full_cache
from apps.memory_api.services.rae_core_service import RAECoreService

# Setup OpenTelemetry (before app creation)
setup_opentelemetry()
instrument_libraries()


# --- Lifespan Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan (startup and shutdown)."""
    # Setup structured logging within lifespan
    setup_logging()
    logger = structlog.get_logger(__name__)

    # Startup
    logger.info("Starting up RAE Memory API...")
    logger.info(
        "security_settings",
        api_key_auth=settings.ENABLE_API_KEY_AUTH,
        jwt_auth=settings.ENABLE_JWT_AUTH,
        rate_limiting=settings.ENABLE_RATE_LIMITING,
    )

    # 1. Initialize Connections
    app.state.pool = await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )

    # Initialize Redis client
    app.state.redis_client = await create_redis_client(settings.REDIS_URL)

    # Initialize Async Qdrant client (Single source of truth)
    from qdrant_client import AsyncQdrantClient

    app.state.qdrant_client = AsyncQdrantClient(
        host=settings.QDRANT_HOST, port=settings.QDRANT_PORT
    )

    # Ensure Qdrant Schema exists before validation (Bootstrap)
    if settings.RAE_DB_MODE in ["validate", "init", "migrate"]:
        try:
            from qdrant_client.http import models as rest

            from apps.memory_api.core.contract_definition import RAE_MEMORY_CONTRACT_V1

            if RAE_MEMORY_CONTRACT_V1.vector_store:
                # Check connectivity first (fast fail if down)
                collections_resp = await app.state.qdrant_client.get_collections()
                existing_collections = {c.name for c in collections_resp.collections}

                for col in RAE_MEMORY_CONTRACT_V1.vector_store.collections:
                    if col.name not in existing_collections:
                        logger.info(
                            f"Auto-creating missing Qdrant collection: {col.name}"
                        )
                        # Map string distance to Qdrant Enum
                        distance_map = {
                            "Cosine": rest.Distance.COSINE,
                            "Euclid": rest.Distance.EUCLID,
                            "Dot": rest.Distance.DOT,
                        }
                        metric = distance_map.get(
                            col.distance_metric, rest.Distance.COSINE
                        )

                        await app.state.qdrant_client.create_collection(
                            collection_name=col.name,
                            vectors_config={
                                "dense": rest.VectorParams(
                                    size=col.vector_size,
                                    distance=metric,
                                )
                            },
                            sparse_vectors_config={
                                "text": rest.SparseVectorParams(),
                            },
                        )
        except Exception as e:
            logger.error(f"Failed to auto-initialize Qdrant schema: {e}")
            # We continue; validation step will catch any remaining issues and Fail Fast

    # 2. Database Initialization / Migration
    if settings.RAE_DB_MODE in ["init", "migrate"]:
        logger.info("db_migration_start", mode=settings.RAE_DB_MODE)
        try:
            import asyncio

            from alembic import command, config

            # Run Alembic migrations programmatically
            # We run this in a thread because Alembic is synchronous
            alembic_cfg = config.Config("alembic.ini")
            await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
            logger.info("db_migration_success")
        except Exception as e:
            logger.error("db_migration_failed", error=str(e))
            raise RuntimeError(f"Database migration failed: {e}") from e

    # 3. Memory Contract Validation (Fail Fast)
    # Validate if mode is 'validate', 'init', or 'migrate' (verify after migration)
    if settings.RAE_DB_MODE in ["validate", "init", "migrate"]:
        logger.info("memory_validation_start", mode=settings.RAE_DB_MODE)

        from apps.memory_api.adapters.postgres_adapter import PostgresAdapter
        from apps.memory_api.adapters.qdrant_adapter import QdrantAdapter
        from apps.memory_api.adapters.redis_adapter import RedisAdapter
        from apps.memory_api.core.contract_definition import RAE_MEMORY_CONTRACT_V1
        from apps.memory_api.services.validation_service import ValidationService

        adapters = [
            PostgresAdapter(app.state.pool),
            RedisAdapter(app.state.redis_client),
            QdrantAdapter(app.state.qdrant_client),
        ]
        validation_service = ValidationService(adapters)
        result = await validation_service.validate_all(RAE_MEMORY_CONTRACT_V1)

        if not result.valid:
            violations_summary = "\n".join(
                [
                    f"- [{v.issue_type}] {v.entity}: {v.details}"
                    for v in result.violations
                ]
            )
            error_msg = (
                f"Memory Contract Validation Failed: {len(result.violations)} violations found.\n"
                f"Violations:\n{violations_summary}\n\n"
                "CRITICAL: The database schema does not match the RAE Memory Contract.\n"
                "HINT: To automatically fix the schema (if possible), set the environment variable:\n"
                "      RAE_DB_MODE=migrate\n"
                "      and restart the container."
            )
            logger.error(
                "memory_validation_failed",
                violations=[v.model_dump() for v in result.violations],
            )
            # Raise exception to stop startup (Fail Fast)
            raise RuntimeError(error_msg)

        logger.info("memory_validation_success")
    elif settings.RAE_DB_MODE == "ignore":
        logger.warning("memory_validation_skipped", mode=settings.RAE_DB_MODE)

    # Initialize RAE-Core service
    app.state.rae_core_service = RAECoreService(
        postgres_pool=app.state.pool,
        qdrant_client=app.state.qdrant_client,
        redis_client=app.state.redis_client,
    )
    logger.info("RAE-Core service initialized")

    await rebuild_full_cache()

    yield  # Application is running

    # Shutdown
    logger.info("Shutting down RAE Memory API...")
    await app.state.pool.close()
    await app.state.redis_client.aclose()  # Close Redis client
    await app.state.qdrant_client.close()  # Close Qdrant client


# --- App Initialization ---
app = FastAPI(
    title="RAE Memory API",
    version="2.2.0-enterprise",
    lifespan=lifespan,
    description="""
    ## The Cognitive Memory Engine for AI Agents

    RAE provides a sophisticated memory system that allows AI agents to:
    - 🧠 Remember past interactions
    - 🔍 Learn from experience
    - 📊 Build knowledge graphs
    - 🎯 Make context-aware decisions

    ### Quick Links
    - [Python SDK](https://github.com/dreamsoft-pro/RAE-agentic-memory/tree/main/sdk/python)
    - [MCP Integration](https://github.com/dreamsoft-pro/RAE-agentic-memory/tree/main/integrations/mcp-server)
    - [Examples](https://github.com/dreamsoft-pro/RAE-agentic-memory/tree/main/examples)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    dependencies=(
        [Depends(auth.verify_token)]
        if settings.ENABLE_API_KEY_AUTH or settings.ENABLE_JWT_AUTH
        else []
    ),
)

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# Add rate limiter to app state
app.state.limiter = limiter

# Add rate limit exception handler
app.add_exception_handler(RateLimitExceeded, cast(Any, rate_limit_exceeded_handler))

# Module-level logger for exception handlers
logger = structlog.get_logger(__name__)


# Custom OpenAPI schema
def custom_openapi():
    """Customize OpenAPI schema with enhanced documentation."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="RAE Memory API",
        version="2.2.0-enterprise",
        description=app.description,
        routes=app.routes,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token authentication",
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key authentication",
        },
    }

    # Add tags descriptions
    openapi_schema["tags"] = [
        {"name": "Health", "description": "Health checks and system metrics"},
        {
            "name": "Memory",
            "description": "Store and query memories across different memory layers",
        },
        {
            "name": "Agent",
            "description": "Agent-specific operations and context management",
        },
        {
            "name": "Cache",
            "description": "Context cache operations for cost optimization",
        },
        {"name": "Graph", "description": "Knowledge graph operations (GraphRAG)"},
        {"name": "Governance", "description": "Cost tracking, budgets, and governance"},
        {
            "name": "ISO/IEC 42001 Compliance",
            "description": "AI governance: human approval workflows, context provenance, circuit breakers, policy management",
        },
        {
            "name": "Event Triggers",
            "description": "Event-driven automation with triggers, conditions, and actions",
        },
        {
            "name": "Reflections",
            "description": "Hierarchical reflection system with clustering and relationship management",
        },
        {
            "name": "Hybrid Search",
            "description": "Multi-strategy search combining vector, semantic, graph, and full-text search",
        },
        {
            "name": "Evaluation",
            "description": "Search quality metrics, A/B testing, and drift detection",
        },
        {
            "name": "Dashboard",
            "description": "Real-time monitoring, visualizations, and WebSocket updates",
        },
        {
            "name": "Graph Management",
            "description": "Advanced graph operations: snapshots, traversal, analytics, and batch operations",
        },
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# --- Exception Handlers ---


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        "http_exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": str(exc.status_code), "message": exc.detail}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "validation_error",
        errors=exc.errors(),
        path=request.url.path,
        method=request.method,
    )
    from fastapi import status
    from fastapi.encoders import jsonable_encoder

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "error": {
                    "code": "422",
                    "message": "Validation Error",
                    "details": exc.errors(),
                },
            }
        ),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception", exc_info=exc)
    from fastapi import status

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "error": {
                "code": "500",
                "message": "Internal Server Error",
            },
        },
    )


# --- Middleware Configuration ---

# CORS Middleware - must be added before other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
if settings.ENABLE_RATE_LIMITING:
    app.middleware("http")(rate_limit_middleware)
    logger.info(
        "rate_limiting_enabled",
        max_requests=settings.RATE_LIMIT_REQUESTS,
        window_seconds=settings.RATE_LIMIT_WINDOW,
    )

# Tenant context middleware
app.add_middleware(TenantContextMiddleware)

# Budget Enforcement middleware (blocks requests if budget exceeded)
app.add_middleware(BudgetEnforcementMiddleware)

# OpenTelemetry instrumentation
instrument_fastapi(app)


# --- API Routes ---

# Health and monitoring endpoints (no auth required)
app.include_router(health_router.router, tags=["Health"])

# API v1 endpoints - Core
app.include_router(memory.router, prefix="/v1", tags=["Memory"])
app.include_router(agent.router, prefix="/v1", tags=["Agent"])
app.include_router(cache.router, prefix="/v1", tags=["Cache"])
app.include_router(graph.router, prefix="/v1", tags=["Graph"])
app.include_router(feedback.router, prefix="/v1", tags=["Feedback"])
app.include_router(governance.router, tags=["Governance"])
app.include_router(compliance.router, tags=["ISO/IEC 42001 Compliance"])

# API v1 endpoints - Enterprise Features
app.include_router(event_triggers.router, tags=["Event Triggers"])
app.include_router(reflections.router, tags=["Reflections"])
app.include_router(hybrid_search.router, tags=["Hybrid Search"])
app.include_router(evaluation.router, tags=["Evaluation"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(graph_enhanced.router, tags=["Graph Management"])
app.include_router(token_savings.router, tags=["Metrics"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    API root endpoint with basic information.
    """
    return {
        "name": "RAE Memory API",
        "version": "1.0.0",
        "description": "Reflective Agentic Memory Engine - Cognitive memory system for AI agents",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
    }
