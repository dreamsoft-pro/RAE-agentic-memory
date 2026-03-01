import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/apps/memory_api/api/v2/memory.py'

with open(path, 'r') as f:
    content = f.read()

# Dodajemy model requestu
old_models = '''class ListMemoryResponseV2(BaseModel):
    """Paginated list of memories."""
    results: list[MemoryResult]
    total: int
    limit: int
    offset: int'''

new_models = '''class ListMemoryResponseV2(BaseModel):
    """Paginated list of memories."""
    results: list[MemoryResult]
    total: int
    limit: int
    offset: int

class UpdateMemoryRequestV2(BaseModel):
    """Update memory request for v2 API."""
    content: str | None = None
    importance: float | None = None
    tags: list[str] | None = None'''

# Dodajemy endpoint
old_route = '''@router.get("/{memory_id}", response_model=MemoryResult)
async def get_memory('''

new_route = '''@router.patch("/{memory_id}")
async def update_memory(
    memory_id: str,
    request: UpdateMemoryRequestV2,
    tenant_id: UUID = Depends(get_and_verify_tenant_id),
    rae_service: RAECoreService = Depends(get_rae_core_service),
):
    """Update memory fields."""
    try:
        updated = await rae_service.update_memory(
            memory_id, str(tenant_id), **request.dict(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"message": "Memory updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("update_memory_failed", memory_id=memory_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{memory_id}", response_model=MemoryResult)
async def get_memory('''

if old_models in content and old_route in content:
    content = content.replace(old_models, new_models)
    content = content.replace(old_route, new_route)
    with open(path, 'w') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED: Models or route not found.")
