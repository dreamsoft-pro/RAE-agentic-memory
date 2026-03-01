import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/rae_adapters/postgres.py'

with open(path, 'r') as f:
    content = f.read()

old_stub = '''    async def update_memory(self, *args, **kwargs) -> bool:
        return True'''

new_impl = '''    async def update_memory(self, memory_id: UUID, tenant_id: str, **kwargs: Any) -> bool:
        pool = await self._get_pool()
        
        set_parts = []
        params = [memory_id, tenant_id]
        
        # Obsługujemy pola, które chcemy aktualizować
        if "tags" in kwargs:
            set_parts.append(f"tags = ${len(params) + 1}")
            params.append(kwargs["tags"])
            
        if "importance" in kwargs:
            set_parts.append(f"importance = ${len(params) + 1}")
            params.append(kwargs["importance"])

        if "content" in kwargs:
            set_parts.append(f"content = ${len(params) + 1}")
            params.append(kwargs["content"])
            
        if not set_parts:
            return False
            
        set_clause = ", ".join(set_parts)
        sql = f"UPDATE memories SET {set_clause} WHERE id = $1 AND tenant_id = $2"
        
        async with pool.acquire() as conn:
            result = await conn.execute(sql, *params)
            return result == "UPDATE 1"'''

if old_stub in content:
    new_content = content.replace(old_stub, new_impl)
    with open(path, 'w') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("FAILED: Stub not found.")
