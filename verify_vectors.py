import asyncio
from qdrant_client import AsyncQdrantClient
from uuid import UUID

async def verify():
    client = AsyncQdrantClient(url="http://localhost:6333")
    collections = await client.get_collections()
    print(f"Collections: {collections}")
    
    info = await client.get_collection("memories")
    print(f"Collection Info: {info.config.params.vectors}")
    
    count = await client.count("memories")
    print(f"Total points: {count.count}")
    
    points = await client.scroll("memories", limit=5, with_vectors=True)
    for p in points[0]:
        print(f"Point {p.id}: Vectors present: {list(p.vector.keys()) if isinstance(p.vector, dict) else 'Single vector'}")
        if isinstance(p.vector, dict):
            for name, vec in p.vector.items():
                print(f"  - {name}: dim {len(vec)}")

if __name__ == "__main__":
    asyncio.run(verify())