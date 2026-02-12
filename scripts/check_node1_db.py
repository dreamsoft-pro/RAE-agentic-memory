import asyncio
import asyncpg

async def main():
    try:
        conn = await asyncpg.connect('postgresql://rae:rae_password@localhost/rae')
        res = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'memories'")
        columns = [r['column_name'] for r in res]
        print(f"COLUMNS: {columns}")
        
        # Check for unique constraint
        res_idx = await conn.fetch("SELECT indexname FROM pg_indexes WHERE tablename = 'memories'")
        print(f"INDEXES: {[r['indexname'] for r in res_idx]}")
        
        await conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
