from typing import List

from fastapi import APIRouter, Depends
from uuid import UUID

from apps.memory_api.dependencies import get_rae_core_service
from apps.memory_api.security import auth
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services.rae_core_service import RAECoreService

router = APIRouter(
    prefix="/system",
    tags=["System"],
    dependencies=[Depends(auth.verify_token)],
)


@router.get("/tenants", response_model=List[str])
async def list_tenants(
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    List all unique tenant IDs.
    """
    return await rae_service.list_unique_tenants()


@router.get("/projects", response_model=List[str])
async def list_projects(
    tenant_id: UUID = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """
    List all unique project IDs for the authenticated tenant.
    """
    return await rae_service.list_unique_projects(tenant_id=tenant_id)
