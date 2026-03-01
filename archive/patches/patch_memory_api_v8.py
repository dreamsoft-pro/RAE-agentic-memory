import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/apps/memory_api/api/v2/memory.py'

with open(path, 'r') as f:
    content = f.read()

NL = chr(10)

model_code = NL + 'class UpdateMemoryRequestV2(BaseModel):' + NL + '    """Update memory request for v2 API."""' + NL + '    content: str | None = None' + NL + '    importance: float | None = None' + NL + '    tags: list[str] | None = None' + NL

route_code = NL + '@router.patch("/{memory_id}")' + NL + 'async def update_memory(' + NL + '    memory_id: str,' + NL + '    request: UpdateMemoryRequestV2,' + NL + '    tenant_id: UUID = Depends(get_and_verify_tenant_id),' + NL + '    rae_service: RAECoreService = Depends(get_rae_core_service),' + NL + '):' + NL + '    """Update memory fields."""' + NL + '    try:' + NL + '        updated = await rae_service.update_memory(' + NL + '            memory_id, str(tenant_id), **request.dict(exclude_unset=True)' + NL + '        )' + NL + '        if not updated:' + NL + '            raise HTTPException(status_code=404, detail="Memory not found")' + NL + '        return {"message": "Memory updated successfully"}' + NL + '    except HTTPException:' + NL + '        raise' + NL + '    except Exception as e:' + NL + '        logger.error("update_memory_failed", memory_id=memory_id, error=str(e))' + NL + '        raise HTTPException(status_code=500, detail=str(e))' + NL

if "class UpdateMemoryRequestV2" not in content:
    content = content.replace('offset: int', 'offset: int' + model_code)

if "@router.patch" not in content:
    target = '@router.get("/{memory_id}"'
    content = content.replace(target, route_code + NL + target)

with open(path, 'w') as f:
    f.write(content)
print("SUCCESS")
