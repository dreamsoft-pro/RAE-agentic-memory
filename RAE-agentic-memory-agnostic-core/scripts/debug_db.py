import os
import asyncio
import asyncpg
import json

async def check():
    url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@postgres/rae")
    conn = await asyncpg.connect(url)
    row = await conn.fetchrow("SELECT metadata FROM memories LIMIT 1")
    print(f"TYPE: {type(row[0])}")
    print(f"CONTENT: {row[0]}")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check())
