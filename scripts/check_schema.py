import os
import asyncio
import asyncpg

async def check():
    url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@postgres/rae")
    conn = await asyncpg.connect(url)
    res = await conn.fetchval("SELECT data_type FROM information_schema.columns WHERE table_name = 'memories' AND column_name = 'metadata'")
    print(f"COLUMN TYPE: {res}")
    
    # Also check a row raw value
    row = await conn.fetchrow("SELECT metadata FROM memories LIMIT 1")
    if row:
        print(f"RAW VALUE TYPE: {type(row[0])}")
        print(f"RAW VALUE: {row[0]}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check())
