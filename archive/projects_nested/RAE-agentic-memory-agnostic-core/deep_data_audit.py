import asyncio
import asyncpg
import os

async def audit():
    # Use environment variables if possible, or fallback to 'postgres' for docker
    db_host = os.getenv("POSTGRES_HOST", "postgres")
    conn = await asyncpg.connect(f"postgresql://rae:rae_password@{db_host}:5432/rae")
    
    # 1. Exact content duplicates
    print("--- Exact Content Duplicates ---")
    rows = await conn.fetch("""
        SELECT content, COUNT(*) as count 
        FROM memories 
        GROUP BY content 
        HAVING COUNT(*) > 1 
        ORDER BY count DESC 
        LIMIT 10
    """)
    for row in rows:
        print(f"Count: {row['count']} | Content: {row['content'][:100]}...")
        
    # 2. Metadata quality
    print("\n--- Metadata Quality ---")
    rows = await conn.fetch("""
        SELECT 
            COUNT(*) FILTER (WHERE metadata IS NULL OR metadata = '{}') as empty_meta,
            COUNT(*) FILTER (WHERE metadata->>'id' IS NULL) as missing_orig_id,
            COUNT(*) as total
        FROM memories
    """)
    row = rows[0]
    print(f"Total memories: {row['total']}")
    print(f"Empty metadata: {row['empty_meta']}")
    print(f"Missing original ID in meta: {row['missing_orig_id']}")

    # 3. Check for short/low quality content
    print("\n--- Low Quality Content (Short) ---")
    rows = await conn.fetch("""
        SELECT content, length(content) as len
        FROM memories
        WHERE length(content) < 20
        LIMIT 5
    """)
    for row in rows:
        print(f"Len: {row['len']} | Content: {row['content']}")

    await conn.close()

if __name__ == "__main__":
    asyncio.run(audit())
