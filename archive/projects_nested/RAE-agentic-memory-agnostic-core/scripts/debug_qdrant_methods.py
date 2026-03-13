import asyncio

from qdrant_client import AsyncQdrantClient


async def main():
    client = AsyncQdrantClient(":memory:")
    print(f"Has search: {hasattr(client, 'search')}")
    print(f"Has query_points: {hasattr(client, 'query_points')}")
    print(f"Dir: {dir(client)}")
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
