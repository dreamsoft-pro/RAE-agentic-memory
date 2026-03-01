import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/apps/memory_api/services/rae_core_service.py'

with open(path, 'r') as f:
    content = f.read()

old_ref = '''    async def get_memory(
        self, memory_id: str, tenant_id: str
    ) -> Optional[Dict[str, Any]]:'''

new_method = '''    async def update_memory(
        self, memory_id: str, tenant_id: str, **kwargs: Any
    ) -> bool:
        """Update an existing memory."""
        try:
            mem_uuid = UUID(memory_id)
        except ValueError:
            return False
        return await self.postgres_adapter.update_memory(mem_uuid, tenant_id, **kwargs)

    async def get_memory('''

if old_ref in content:
    new_content = content.replace(old_ref, new_method)
    with open(path, 'w') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("FAILED: Reference point not found.")
