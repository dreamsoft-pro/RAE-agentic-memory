import asyncio

from qdrant_client import AsyncQdrantClient


async def test():
    try:
        client = AsyncQdrantClient(host="127.0.0.1", port=6333)
        collections = await client.get_collections()
        print(f"✅ Qdrant Connection Successful: {collections}")
    except Exception as e:
        print(f"❌ Qdrant Connection Failed: {e}")


if __name__ == "__main__":
    asyncio.run(test())
