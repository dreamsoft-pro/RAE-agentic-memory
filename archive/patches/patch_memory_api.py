import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/apps/memory_api/api/v2/memory.py'
if not os.path.exists(path):
    path = '/app/apps/memory_api/api/v2/memory.py'

with open(path, 'r') as f:
    content = f.read()

old_func = '''@router.get("/", response_model=ListMemoryResponseV2)
async def list_memories(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    project: Optional[str] = None,
    layer: Optional[str] = None,
    tenant_id: UUID = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """List memories with pagination."""
    try:
        memories = await rae_service.list_memories(
            tenant_id=str(tenant_id),
            limit=limit,
            offset=offset,
            project=project,
            layer=layer,
        )'''

new_func = '''@router.get("/", response_model=ListMemoryResponseV2)
async def list_memories(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    project: Optional[str] = None,
    layer: Optional[str] = None,
    tag: Optional[list[str]] = Query(None),
    tenant_id: UUID = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """List memories with pagination."""
    try:
        memories = await rae_service.list_memories(
            tenant_id=str(tenant_id),
            limit=limit,
            offset=offset,
            project=project,
            layer=layer,
            tags=tag,
        )'''

if old_func in content:
    new_content = content.replace(old_func, new_func)
    with open(path, 'w') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("FAILED: Content not found exactly.")
