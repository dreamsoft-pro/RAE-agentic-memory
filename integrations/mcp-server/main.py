import os
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel

from .rae_client import RAEClient
from .watcher import start_watching


# --- Application Lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    app.state.watched_projects = {}
    print("MCP Server starting up...")
    yield
    # Shutdown: Cleanup resources
    print("MCP Server shutting down...")
    for project_id, project_data in app.state.watched_projects.items():
        if project_data.get("observer"):
            project_data["observer"].stop()
            project_data["observer"].join()
            print(f"Stopped watcher for project: {project_id}")


app = FastAPI(
    title="MCP (Memory Context Provider) Server",
    description="A local daemon that watches project files and feeds them into the RAE Memory Engine.",
    version="0.1.0",
    lifespan=lifespan,
)


# --- API Models ---
class Project(BaseModel):
    path: str
    tenant_id: str  # Each project should have its own tenant_id


class ProjectRegistrationResponse(BaseModel):
    project_id: str
    message: str


# --- Helper Functions ---
def get_file_update_callback(tenant_id: str):
    """
    Creates a callback function for the file watcher.
    The callback will instantiate a RAEClient and store the file content.
    """

    def callback(file_path: str):
        print(f"File change detected for tenant {tenant_id}: {file_path}")
        rae_client = RAEClient(tenant_id=tenant_id)
        rae_client.store_file_memory(file_path)

    return callback


# --- API Endpoints ---


@app.get("/status")
async def get_status():
    """
    Returns the current status of the MCP server.
    """
    project_count = len(app.state.watched_projects)
    return {"status": "running", "watched_projects_count": project_count}


@app.post("/projects", response_model=ProjectRegistrationResponse)
async def register_project(project: Project, background_tasks: BackgroundTasks):
    """
    Registers a new project directory to be watched.
    """
    path = os.path.abspath(project.path)
    if not os.path.isdir(path):
        raise HTTPException(
            status_code=400, detail="The provided path is not a valid directory."
        )

    project_id = f"{project.tenant_id}-{os.path.basename(path)}"
    if project_id in app.state.watched_projects:
        raise HTTPException(
            status_code=400, detail=f"Project '{project_id}' is already being watched."
        )

    callback = get_file_update_callback(tenant_id=project.tenant_id)
    observer = start_watching(path, callback)

    app.state.watched_projects[project_id] = {
        "path": path,
        "tenant_id": project.tenant_id,
        "observer": observer,
    }

    print(f"Started watching project: {project_id} at {path}")

    return ProjectRegistrationResponse(
        project_id=project_id, message=f"Started watching project '{project_id}'."
    )


@app.get("/projects")
async def list_projects():
    """
    Lists all projects currently being watched.
    """
    # Return a serializable version of the watched_projects dict
    return {
        pid: {"path": data["path"], "tenant_id": data["tenant_id"]}
        for pid, data in app.state.watched_projects.items()
    }


@app.delete("/projects/{project_id}")
async def unregister_project(project_id: str):
    """
    Stops watching a project directory.
    """
    if project_id not in app.state.watched_projects:
        raise HTTPException(status_code=404, detail="Project not found.")

    project_data = app.state.watched_projects[project_id]
    observer = project_data.get("observer")
    if observer:
        observer.stop()
        observer.join()

    del app.state.watched_projects[project_id]

    print(f"Stopped watching project: {project_id}")

    return {"message": f"Stopped watching project '{project_id}'."}


# --- RAE API Proxy Endpoints ---


class StoreMemoryRequest(BaseModel):
    content: str
    source: str
    layer: str = "ltm"
    tags: list = []
    project: str


class QueryMemoryRequest(BaseModel):
    query_text: str
    k: int = 10


class DeleteMemoryRequest(BaseModel):
    memory_id: str


@app.post("/memory/store")
def store_memory_proxy(req: StoreMemoryRequest, tenant_id: str):
    """
    Proxy endpoint to store memory in the RAE API.
    """
    rae_client = RAEClient(tenant_id=tenant_id)
    # The client's store_file_memory is not a perfect fit,
    # as it reads from a file. We'll adapt by just using its payload structure.
    payload = {
        "content": req.content,
        "source": req.source,
        "layer": req.layer,
        "tags": req.tags,
        "project": req.project,
    }
    # This requires a method in RAEClient that directly posts a payload.
    # Let's assume we'll add `store_memory(self, payload)` to RAEClient.
    # For now, we'll manually construct the request.
    with httpx.Client() as client:
        response = client.post(
            f"{rae_client.base_v1_url}/memory/store",
            json=payload,
            headers=rae_client.headers,
        )
        response.raise_for_status()
        return response.json()


@app.post("/memory/query")
def query_memory_proxy(req: QueryMemoryRequest, tenant_id: str):
    """
    Proxy endpoint to query memory from the RAE API.
    """
    rae_client = RAEClient(tenant_id=tenant_id)
    return rae_client.query_memory(req.query_text, req.k)


@app.delete("/memory/delete")
def delete_memory_proxy(req: DeleteMemoryRequest, tenant_id: str):
    """
    Proxy endpoint to delete memory from the RAE API.
    """
    rae_client = RAEClient(tenant_id=tenant_id)
    return rae_client.delete_memory(req.memory_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
