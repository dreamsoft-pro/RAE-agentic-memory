import asyncio
import asyncpg
import hashlib
import os
import json

async def deep_clean():
    host = os.getenv("POSTGRES_HOST", "rae-postgres")
    db = os.getenv("POSTGRES_DB", "rae")
    user = os.getenv("POSTGRES_USER", "rae")
    pw = os.getenv("POSTGRES_PASSWORD", "rae_password")
    
    conn = await asyncpg.connect(f'postgresql://{user}:{pw}@{host}/{db}')
    print("🧹 Silicon Oracle: Starting DEEP CLEAN procedure...")
    
    # 1. Fetch all memories
    rows = await conn.fetch("SELECT id, content, tenant_id, metadata, usage_count, importance FROM memories")
    print(f"   Analyzing {len(rows)} records...")
    
    seen = {} # (tenant_id, content_hash) -> master_record
    to_delete = []
    
    for r in rows:
        ch = hashlib.sha256(r['content'].encode('utf-8')).hexdigest()
        key = (r['tenant_id'], ch)
        
        if key in seen:
            master = seen[key]
            # Consolidate stats
            master['usage_count'] += (r['usage_count'] or 1)
            master['importance'] = max(master['importance'], r['importance'] or 0.5)
            to_delete.append(r['id'])
        else:
            seen[key] = {
                'id': r['id'],
                'content_hash': ch,
                'usage_count': r['usage_count'] or 1,
                'importance': r['importance'] or 0.5
            }
            
    print(f"   Found {len(to_delete)} duplicate records to merge.")
    
    # 2. Update masters and delete duplicates
    for key, m in seen.items():
        await conn.execute(
            "UPDATE memories SET content_hash = $1, usage_count = $2, importance = $3 WHERE id = $4",
            m['content_hash'], m['usage_count'], m['importance'], m['id']
        )
        
    if to_delete:
        await conn.execute("DELETE FROM memories WHERE id = ANY($1)", to_delete)
        print(f"✅ Successfully merged and deleted {len(to_delete)} duplicates.")
    
    print("✨ Silicon Oracle is now CLEAN and CONSISTENT.")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(deep_clean())
