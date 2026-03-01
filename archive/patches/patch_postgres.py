import sys
import os

path = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/rae_adapters/postgres.py'
if not os.path.exists(path):
    path = '/app/rae_adapters/postgres.py' # fallback for inside container if needed, but we are on host

with open(path, 'r') as f:
    content = f.read()

old_list = '''    async def list_memories(
        self, tenant_id: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        limit = kwargs.get("limit", 100)
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM memories WHERE tenant_id = $1 LIMIT $2", tenant_id, limit
            )
        return [dict(r) for r in rows]'''

new_list = '''    async def list_memories(
        self, tenant_id: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        limit = kwargs.get("limit", 100)
        offset = kwargs.get("offset", 0)
        layer = kwargs.get("layer")
        project = kwargs.get("project") or kwargs.get("agent_id")
        tags = kwargs.get("tags")
        
        where_parts = ["tenant_id = $1"]
        params = [tenant_id]
        
        if layer:
            where_parts.append(f"layer = ${len(params) + 1}")
            params.append(layer)
            
        if project:
            where_parts.append(f"(project = ${len(params) + 1} OR agent_id = ${len(params) + 1})")
            params.append(project)
            
        if tags:
            where_parts.append(f"tags @> ${len(params) + 1}")
            params.append(tags)
            
        where_clause = " AND ".join(where_parts)
        
        sql = f"SELECT * FROM memories WHERE {where_clause} ORDER BY created_at DESC LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}"
        params.extend([limit, offset])
        
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [dict(r) for r in rows]'''

if old_list in content:
    new_content = content.replace(old_list, new_list)
    with open(path, 'w') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("FAILED: Content not found exactly.")
