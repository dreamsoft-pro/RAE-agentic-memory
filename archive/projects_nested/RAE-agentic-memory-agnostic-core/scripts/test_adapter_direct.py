import os
import asyncio
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path("/app")
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))

from rae_adapters.postgres import PostgreSQLStorage

async def test():
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@postgres/rae")
    storage = PostgreSQLStorage(db_url)
    
    print("Fetching memories via list_memories...")
    mems = await storage.list_memories("00000000-0000-0000-0000-000000000000", limit=1)
    if mems:
        m = mems[0]
        print(f"Memory keys: {m.keys()}")
        print(f"Metadata type: {type(m.get('metadata'))}")
        print(f"Metadata value: {m.get('metadata')}")
    else:
        print("No memories found!")

if __name__ == "__main__":
    asyncio.run(test())
