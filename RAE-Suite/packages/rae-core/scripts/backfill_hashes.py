import asyncio
import asyncpg
import hashlib
import os

async def backfill_hashes():
    # Use environment variables if available, fallback to container defaults
    host = os.getenv("POSTGRES_HOST", "rae-postgres")
    db = os.getenv("POSTGRES_DB", "rae")
    user = os.getenv("POSTGRES_USER", "rae")
    pw = os.getenv("POSTGRES_PASSWORD", "rae_password")
    
    print(f"🛠 Repairing Silicon Oracle: Connecting to {host}...")
    try:
        conn = await asyncpg.connect(f'postgresql://{user}:{pw}@{host}/{db}')
        
        rows = await conn.fetch("SELECT id, content FROM memories WHERE content_hash IS NULL")
        print(f"   Found {len(rows)} memories to repair.")
        
        for r in rows:
            ch = hashlib.sha256(r['content'].encode('utf-8')).hexdigest()
            await conn.execute("UPDATE memories SET content_hash = $1 WHERE id = $2", ch, r['id'])
        
        print("✅ All hashes backfilled!")
        await conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(backfill_hashes())