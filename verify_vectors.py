import asyncio
import os

from qdrant_client import AsyncQdrantClient


async def main():
    client = AsyncQdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)
    collection = "synergy_final"
    print(f"🔍 Inspecting collection: {collection}")

    try:
        res = await client.scroll(
            collection_name=collection, limit=5, with_payload=True, with_vectors=False
        )
        points = res[0]
        for p in points:
            print(f"ID: {p.id}")
            print(f"Payload: {p.payload}")
            print("-" * 20)
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
