import asyncio

import asyncpg


async def test():
    try:
        conn = await asyncpg.connect(
            user="rae",
            password="rae_password",
            database="rae",
            host="127.0.0.1",
            port=5432,
        )
        print("✅ Postgres Connection Successful")
        await conn.close()
    except Exception as e:
        print(f"❌ Postgres Connection Failed: {e}")


if __name__ == "__main__":
    asyncio.run(test())
