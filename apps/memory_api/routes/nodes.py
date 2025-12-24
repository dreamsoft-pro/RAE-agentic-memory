from typing import Optional
from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Request

from apps.memory_api.dependencies import get_db_pool
from apps.memory_api.models.control_plane import (
    ComputeNode,
    CreateTaskRequest,
    DelegatedTask,
    HeartbeatRequest,
    RegisterNodeRequest,
    TaskResultRequest,
)
from apps.memory_api.repositories.node_repository import NodeRepository
from apps.memory_api.repositories.task_repository import TaskRepository
from apps.memory_api.services.control_plane_service import ControlPlaneService

router = APIRouter(prefix="/control", tags=["Control Plane"])


def get_control_plane_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> ControlPlaneService:
    node_repo = NodeRepository(pool)
    task_repo = TaskRepository(pool)
    return ControlPlaneService(node_repo, task_repo)


@router.post("/tasks", response_model=DelegatedTask, status_code=201)
async def create_task(
    req: CreateTaskRequest,
    service: ControlPlaneService = Depends(get_control_plane_service),
):
    """
    Create a new task for delegation to a compute node.
    """
    try:
        return await service.create_task(
            type=req.type, payload=req.payload, priority=req.priority
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nodes/register", response_model=ComputeNode)
async def register_node(
    req: RegisterNodeRequest,
    request: Request,
    service: ControlPlaneService = Depends(get_control_plane_service),
):
    # Security: Verify IP is from Tailscale (100.x.x.x) or localhost
    client_host = request.client.host if request.client else "unknown"
    # In production, we might want to enforce this check if binding isn't restrictive enough

    return await service.register_node(
        req.node_id, req.api_key, req.capabilities, client_host
    )


@router.post("/nodes/heartbeat", response_model=ComputeNode)
async def heartbeat(
    req: HeartbeatRequest,
    service: ControlPlaneService = Depends(get_control_plane_service),
):
    try:
        return await service.process_heartbeat(req.node_id, req.status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/tasks/poll", response_model=Optional[DelegatedTask])
async def poll_task(
    node_id: str, service: ControlPlaneService = Depends(get_control_plane_service)
):
    try:
        return await service.poll_task(node_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tasks/{task_id}/result", response_model=DelegatedTask)
async def submit_result(
    task_id: UUID,
    req: TaskResultRequest,
    service: ControlPlaneService = Depends(get_control_plane_service),
):
    try:
        if task_id != req.task_id:
            raise HTTPException(status_code=400, detail="Task ID mismatch")
        return await service.submit_result(task_id, req.result, req.error)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
