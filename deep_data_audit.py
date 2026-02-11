import asyncio
from qdrant_client import AsyncQdrantClient
from rae_core.embedding.native import NativeEmbeddingProvider
import os

async def audit():
    client = AsyncQdrantClient(url="http://localhost:6333")
    
    # 1. Check points
    points = await client.scroll("memories", limit=10, with_vectors=True)
    if not points[0]:
        print("❌ NO POINTS IN QDRANT!")
        return
        
    for p in points[0]:
        v_types = list(p.vector.keys()) if isinstance(p.vector, dict) else ["single"]
        print(f"Point {p.id}: {v_types}")
        if isinstance(p.vector, dict):
            for name, vec in p.vector.items():
                v_sum = sum(abs(x) for x in vec[:10])
                print(f"  - {name}: dim {len(vec)}, abs_sum_top10 {v_sum}")

    # 2. Test Search
    project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
    model_path = os.path.join(project_root, "models/all-MiniLM-L6-v2/model.onnx")
    tok_path = os.path.join(project_root, "models/all-MiniLM-L6-v2/tokenizer.json")
    
    provider = NativeEmbeddingProvider(model_path, tok_path)
    query = "disk error"
    emb = await provider.embed_text(query)
    
    print(f"\nSearching for '{query}' in 'dense'...")
    res = await client.search(
        collection_name="memories",
        query_vector=("dense", emb),
        limit=5
    )
    print(f"Results in dense: {len(res)}")
    for r in res:
        print(f"  - {r.id} score {r.score}")

if __name__ == "__main__":
    asyncio.run(audit())