
import asyncio
import os
import sys
from pathlib import Path
from uuid import uuid4, UUID

# Add project root and rae-core to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))

from rae_adapters.postgres import PostgreSQLStorage
from rae_adapters.qdrant import QdrantVectorStore
from rae_core.embedding.native import NativeEmbeddingProvider
from rae_core.embedding.manager import EmbeddingManager
import asyncpg
from qdrant_client import AsyncQdrantClient

from rae_core.math.theories.contract import EvolutionContract

async def test():
    print("🛠️ Testing Multi-Vector Ingest...")
    # RAE-First: Use deterministic UUID v5 from Contract
    tenant_id = EvolutionContract.generate_deterministic_id("TEST-INGEST-369")
    
    # 1. Setup
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@localhost/rae")
    pool = await asyncpg.create_pool(db_url.replace("+asyncpg", ""))
    q_client = AsyncQdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)
    
    storage = PostgreSQLStorage(pool=pool)
    
    minilm = NativeEmbeddingProvider(
        model_path="models/all-MiniLM-L6-v2/model.onnx", 
        tokenizer_path="models/all-MiniLM-L6-v2/tokenizer.json"
    )
    nomic = NativeEmbeddingProvider(
        model_path="models/nomic-embed-text-v1.5/model.onnx", 
        tokenizer_path="models/nomic-embed-text-v1.5/tokenizer.json"
    )
    
    manager = EmbeddingManager(default_provider=minilm, default_model_name="dense")
    manager.register_provider("nomic", nomic)
    
    vector_store = QdrantVectorStore(client=q_client, embedding_dim=384, vector_name="dense")
    await vector_store.setup()
    await vector_store.update_collection_schema({"nomic": 768})
    
    # 2. Ingest
    content = "RAE Multi-Vector Test Memory for industrial logs 0xABC123"
    m_id = uuid4()
    human_label = "Test-MultiVector-Diagnostic-001"
    
    print(f"📥 Storing in Postgres (Label: {human_label})...")
    m_id = await storage.store_memory(
        memory_id=m_id, 
        content=content, 
        tenant_id=tenant_id, 
        agent_id="Test-Agent-369",
        info_class="internal",
        governance={},
        metadata={"test": True, "human_label": human_label}
    )
    print(f"   Stored with ID: {m_id}")
    
    print("🧬 Generating Embeddings...")
    embs = await manager.generate_all_embeddings([content])
    
    print("📡 Storing in Qdrant...")
    await vector_store.add_vector(
        memory_id=m_id,
        embedding={"dense": embs["dense"][0], "nomic": embs["nomic"][0]},
        tenant_id=tenant_id,
        agent_id="Test-Agent-369",
        layer="episodic"
    )
    
    # 3. Verify
    print("🔍 Verifying in Postgres...")
    all_rows = await pool.fetch("SELECT id, content, tenant_id FROM memories WHERE tenant_id = $1", tenant_id)
    print(f"   Debug: Found {len(all_rows)} records for tenant {tenant_id}")
    for r in all_rows:
        print(f"   - {r['id']} | {r['content'][:30]}...")
    
    row = await pool.fetchrow("SELECT content FROM memories WHERE id = $1", m_id)
    print(f"   Postgres: {'✅ Found' if row else '❌ Missing'}")
    
    print("🔍 Verifying Search by HUMAN LABEL (Pillar 1: Logos)...")
    # We use search_memories from Postgres storage directly for this test
    # It should find it via the ILIKE fallback we just added
    res_label = await storage.search_memories(
        query="Test-MultiVector", 
        tenant_id=str(tenant_id), 
        agent_id="Test-Agent-369"
    )
    print(f"   Label Search: {'✅ Found' if any(str(r['id']) == str(m_id) for r in res_label) else '❌ Missing'}")

    print("🔍 Verifying Cross-Layer Search (Layer Gravity)...")
    # Should work when layer is None
    res_all = await storage.search_memories(
        query="ABC123", 
        tenant_id=str(tenant_id), 
        agent_id="Test-Agent-369",
        layer=None
    )
    print(f"   All-Layer Search: {'✅ Found' if any(str(r['id']) == str(m_id) for r in res_all) else '❌ Missing'}")
    
    await pool.close()

if __name__ == "__main__":
    asyncio.run(test())
