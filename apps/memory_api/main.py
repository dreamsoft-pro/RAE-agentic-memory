from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, HTTPException, Request
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
    system,
)
from apps.memory_api.config import settings
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
    federation,
    graph_enhanced,
    hybrid_search,
    nodes,
    reflections,
    sync,
    token_savings,
)
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
    logger = structlog.get_logger("apps.memory_api.main")

    logger.info(
        "Starting up RAE Memory API...",
        profile=settings.RAE_PROFILE,
    )
    logger.info(
        "security_settings",
        api_key_auth=settings.ENABLE_API_KEY_AUTH,
        jwt_auth=settings.ENABLE_JWT_AUTH,
        rate_limiting=settings.ENABLE_RATE_LIMITING,
    )

    # 1. Initialize Connections (via Factory)
    from rae_core.factories.infra_factory import InfrastructureFactory

    await InfrastructureFactory.initialize(app, settings)

    # 2. Setup Background Components
    # Initialize RAE Core Service (Agnostic)
    app.state.rae_core_service = RAECoreService(app.state.pool)

    if settings.RAE_PROFILE == "lite":
        logger.info("lite_mode_active", details="Skipping heavy initialization")
    else:
        # Pre-build cache if not in lite mode
        try:
            await rebuild_full_cache()
            logger.info("cache_rebuilt_successfully")
        except Exception as e:
            logger.error("cache_rebuild_failed", error=str(e))

    logger.info("RAE-Core service initialized", profile=settings.RAE_PROFILE)

    yield

    # Shutdown
    logger.info("Shutting down RAE Memory API...")
    if hasattr(app.state, "pool") and app.state.pool:
        await app.state.pool.close()


# --- FastAPI App Initialization ---
app = FastAPI(
    title="RAE Memory API",
    description="Reflective Agentic Memory Engine - Enterprise API",
    version="2.9.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Middlewares ---

# 1. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Tenant Context
app.add_middleware(TenantContextMiddleware)

# 3. Budget Enforcement (Enterprise)
app.add_middleware(BudgetEnforcementMiddleware)

# 4. Global Rate Limiting (SlowAPI)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)  # type: ignore[arg-type]

# 5. OpenTelemetry Instrumentation
instrument_fastapi(app)

# 6. Prometheus Metrics
Instrumentator().instrument(app).expose(app)


# --- Exception Handlers ---


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "422",
                "message": "Validation Error",
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle standard FastAPI HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": str(exc.status_code), "message": exc.detail}},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected server errors."""
    structlog.get_logger(__name__).error("unhandled_exception", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "500", "message": "Internal Server Error"}},
    )


# --- Routes Registration ---

# Health / Monitoring
app.include_router(health_router.router, tags=["System"])

# API V1
app.include_router(memory.router, prefix="/v1", tags=["Memory Operations"])
app.include_router(agent.router, prefix="/v1", tags=["Agent Integration"])
app.include_router(graph.router, prefix="/v1", tags=["Knowledge Graph"])
app.include_router(governance.router, prefix="/v1", tags=["Governance"])
app.include_router(compliance.router, prefix="/v1", tags=["Compliance"])
app.include_router(feedback.router, prefix="/v1", tags=["Feedback"])
app.include_router(cache.router, prefix="/v1", tags=["Cache Management"])
app.include_router(system.router, prefix="/v1", tags=["System Control"])

# New Routes
app.include_router(dashboard.router, prefix="/v1", tags=["Dashboard"])
app.include_router(evaluation.router, prefix="/v1", tags=["Evaluation"])
app.include_router(event_triggers.router, prefix="/v1", tags=["Automation"])
app.include_router(graph_enhanced.router, prefix="/v1", tags=["Knowledge Graph+"])
app.include_router(hybrid_search.router, prefix="/v1", tags=["Search"])
app.include_router(nodes.router, prefix="/v1", tags=["Knowledge Graph Nodes"])
app.include_router(reflections.router, prefix="/v1", tags=["Reflections"])
app.include_router(sync.router, prefix="/v1", tags=["Sync"])
app.include_router(token_savings.router, prefix="/v1", tags=["Token Savings"])
app.include_router(federation.router, prefix="/v1", tags=["Federation"])


# Custom OpenAPI Schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add Enterprise Customizations
    openapi_schema["info"]["x-logo"] = {"url": "https://rae.ai/logo.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[method-assign]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
