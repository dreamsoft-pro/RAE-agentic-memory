import asyncio
import asyncpg
import socket

async def test_connection(port):
    print(f"Testing port {port}...")
    try:
        conn = await asyncpg.connect(
            host="127.0.0.1",
            port=port,
            user="rae",
            password="rae_password",
            database="rae",
            timeout=5
        )
        print(f"✅ Success on port {port}!")
        await conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed on port {port}: {e}")
        return False

async def main():
    await test_connection(5432)
    await test_connection(5433)

if __name__ == "__main__":
    asyncio.run(main())
