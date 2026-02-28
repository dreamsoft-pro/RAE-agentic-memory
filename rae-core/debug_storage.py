import asyncio
from uuid import uuid4
from rae_core.adapters.postgres import PostgreSQLStorage
from rae_core.adapters.postgres_db import PostgresDatabaseProvider

async def main():
    db = PostgresDatabaseProvider()
    storage = PostgreSQLStorage(pool=db)
    mid = str(uuid4())
    print(f'Attempting to store {mid}...')
    try:
        res = await storage.store_memory(memory_id=mid, content='test', tenant_id='t1', agent_id='a1', project='p1', layer='working')
        print(f'Result: {res}')
    except Exception as e:
        print(f'Error: {e}')

asyncio.run(main())
