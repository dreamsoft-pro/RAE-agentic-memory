import asyncio
import sys
from pathlib import Path

import asyncpg
import yaml
from qdrant_client import AsyncQdrantClient

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "rae-core"))

async def probe():
    print("🕵️  Probing active benchmark state (First 10k snapshot)...")

    # Load queries
    with open("benchmarking/sets/industrial_ultra_200q.yaml", "r") as f:
        # Use safe loader for speed if available
        try:
            from yaml import CSafeLoader as Loader
        except ImportError:
            from yaml import SafeLoader as Loader
        data = yaml.load(f, Loader=Loader)

    queries = data.get("queries", [])[:20] # Test first 20 queries
    # RUNNER USES 'name' from yaml as project_id, but passes it to 'agent_id' param in store_memory
    target_agent_id = "industrial_ultra_200q"
    tenant_id = "00000000-0000-0000-0000-000000000000"

    # Connect to DBs
    pool = await asyncpg.create_pool(
        host="127.0.0.1", port=5432, user="rae", password="rae_password", database="rae"
    )
    qdrant = AsyncQdrantClient(host="127.0.0.1", port=6333)

    from rae_adapters.postgres import PostgreSQLStorage
    from rae_adapters.qdrant import QdrantVectorStore
    from rae_core.embedding.manager import EmbeddingManager
    from rae_core.embedding.native import NativeEmbeddingProvider
    from rae_core.engine import RAEEngine

    # Initialize Engine (Re-using active components)
    model_path = "models/all-MiniLM-L6-v2/model.onnx"
    tokenizer_path = "models/all-MiniLM-L6-v2/tokenizer.json"
    provider = NativeEmbeddingProvider(model_path=model_path, tokenizer_path=tokenizer_path)

    storage = PostgreSQLStorage(pool=pool)
    vector_store = QdrantVectorStore(client=qdrant, embedding_dim=384)
    manager = EmbeddingManager(default_provider=provider)
    engine = RAEEngine(memory_storage=storage, vector_store=vector_store, embedding_provider=manager)

    print(f"🔍 Running 20 Probe Queries against active DB (Agent: {target_agent_id})...")

    hits = 0

    for i, q in enumerate(queries):
        q["expected_source_ids"]

        # Search using agent_id matching the runner's insertion logic
        results = await engine.search_memories(
            query=q["query"],
            tenant_id=tenant_id,
            agent_id=target_agent_id, # Crucial Fix
            top_k=5,
            enable_reranking=False
        )

        # Check if any result ID matches expected IDs
        # Note: In V2/Runner, IDs are preserved.
        [str(r["id"]) for r in results]
        # Also check content because runner might generate new UUIDs if not forced
        # The runner code: m_id = await engine... (generates new UUID)
        # BUT it maps them in memory: self._map_ids_smart
        # We don't have that map here.
        # Fallback: Check if the text matches any of the expected texts (re-deriving)

        # Actually, the runner generates memories with specific IDs "mem_000001" in the YAML
        # But PostgresStorage generates a NEW UUID for the DB row.
        # So we can't match IDs easily without the 'metadata' which might hold the original ID.
        # Let's check metadata.

        found = False
        for r in results:
            # Runner stores original ID in metadata?
            # Runner code: metadata=mem["metadata"] -> metadata: {"component": ...}
            # It DOES NOT store the "id": "mem_..." in metadata by default in the yaml gen?
            # Wait, yaml has "id". Runner:
            # for j, mem in enumerate(batch): ... store_memory(..., metadata=mem.get("metadata", {}))
            # It seems original ID is LOST in DB unless it was in metadata.

            # Let's use Content Matching for the probe
            r_content = r["content"]
            # Expected content logic from generator:
            # text: f"[MES] {comp}: Event {i} occurred..."
            # Query: "Find logs for {target}"
            # This is hard to match exactly without the full dataset map.

            # Simplified "Hit" check: Does the result contain the target keyword?
            # Query: "Find logs for db" -> Target: "db"
            target_term = q["query"].replace("Find logs for ", "")
            if target_term in r_content:
                found = True
                break

        if found:
            hits += 1

        print(f"   Q{i+1}: {q['query']} -> {'✅ HIT' if found else '❌ MISS'}")

    print(f"\n📊 Interim Search Effectiveness (Content-Match Proxy): {hits}/{len(queries)} ({hits/len(queries)*100:.1f}%)")

    await pool.close()

if __name__ == "__main__":
    asyncio.run(probe())
