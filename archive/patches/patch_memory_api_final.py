import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/apps/memory_api/api/v2/memory.py'

with open(path, 'r') as f:
    lines = f.readlines()

new_lines = []
models_added = False
route_added = False

for line in lines:
    if 'class ListMemoryResponseV2(BaseModel):' in line:
        # Znaleźliśmy koniec modeli (zakładamy 5 linii dalej)
        pass
    
    if 'total: int' in line and not models_added:
        new_lines.append(line)
        continue
    
    if 'offset: int' in line and not models_added:
        new_lines.append(line)
        new_lines.append('
')
        new_lines.append('class UpdateMemoryRequestV2(BaseModel):
')
        new_lines.append('    """Update memory request for v2 API."""
')
        new_lines.append('    content: str | None = None
')
        new_lines.append('    importance: float | None = None
')
        new_lines.append('    tags: list[str] | None = None
')
        models_added = True
        continue

    if '@router.get("/{memory_id}"' in line and not route_added:
        new_lines.append('@router.patch("/{memory_id}")
')
        new_lines.append('async def update_memory(
')
        new_lines.append('    memory_id: str,
')
        new_lines.append('    request: UpdateMemoryRequestV2,
')
        new_lines.append('    tenant_id: UUID = Depends(get_and_verify_tenant_id),
')
        new_lines.append('    rae_service: RAECoreService = Depends(get_rae_core_service),
')
        new_lines.append('):
')
        new_lines.append('    """Update memory fields."""
')
        new_lines.append('    try:
')
        new_lines.append('        updated = await rae_service.update_memory(
')
        new_lines.append('            memory_id, str(tenant_id), **request.dict(exclude_unset=True)
')
        new_lines.append('        )
')
        new_lines.append('        if not updated:
')
        new_lines.append('            raise HTTPException(status_code=404, detail="Memory not found")
')
        new_lines.append('        return {"message": "Memory updated successfully"}
')
        new_lines.append('    except HTTPException:
')
        new_lines.append('        raise
')
        new_lines.append('    except Exception as e:
')
        new_lines.append('        logger.error("update_memory_failed", memory_id=memory_id, error=str(e))
')
        new_lines.append('        raise HTTPException(status_code=500, detail=str(e))
')
        new_lines.append('
')
        route_added = True
    
    new_lines.append(line)

if models_added and route_added:
    with open(path, 'w') as f:
        f.writelines(new_lines)
    print("SUCCESS")
else:
    print(f"FAILED: models={models_added}, route={route_added}")
