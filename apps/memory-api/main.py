from fastapi import FastAPI
from .middleware.tenant import TenantContextMiddleware
from .routers import memory, agent

app = FastAPI(title="Agentic Memory API", version="0.1")

app.add_middleware(TenantContextMiddleware)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(memory.router)
app.include_router(agent.router)
