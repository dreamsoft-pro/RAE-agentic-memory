import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/apps/memory_api/api/v2/memory.py'

with open(path, 'r') as f:
    content = f.read()

model_code = """
class UpdateMemoryRequestV2(BaseModel):
    """Update memory request for v2 API."""
    content: str | None = None
    importance: float | None = None
    tags: list[str] | None = None
"""

route_code = """
@router.patch("/{memory_id}")
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
"""

if "class UpdateMemoryRequestV2" not in content:
    content = content.replace("offset: int", "offset: int" + model_code)

if "@router.patch" not in content:
    content = content.replace("@router.get("/{memory_id}"", route_code + "
@router.get("/{memory_id}"")

with open(path, 'w') as f:
    f.write(content)
print("SUCCESS")
