import argparse
import asyncio
import os
import sys
from pathlib import Path
from uuid import UUID

import yaml
import structlog

# Add project root and rae-core to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))

from rae_core.engine import RAEEngine
from rae_core.search.engine import HybridSearchEngine
from rae_core.search.strategies.fulltext import FullTextStrategy
from rae_core.search.strategies.vector import VectorSearchStrategy
from rae_adapters.postgres import PostgreSQLStorage
from rae_adapters.qdrant import QdrantVectorStore
from rae_core.embedding.native import NativeEmbeddingProvider
from rae_core.config.settings import RAESettings as Settings

logger = structlog.get_logger(__name__)

class RAEBenchmarkRunner:
    def __init__(self, dataset_path, tenant_id, queries=100):
        self.dataset_path = Path(dataset_path)
        self.tenant_id = tenant_id
        self.queries = queries
        self.engine = None
        self.pool = None
        self.agent_id = self.dataset_path.stem

    async def setup(self):
        import asyncpg
        from qdrant_client import AsyncQdrantClient
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.search.strategies.multi_vector import MultiVectorSearchStrategy
        
        db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@localhost/rae")
        self.pool = await asyncpg.create_pool(db_url.replace("+asyncpg", ""))
        
        q_client = AsyncQdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)
        storage = PostgreSQLStorage(pool=self.pool)
        
        # 1. Initialize Multiple Models (The Logos & Psyche pillars)
        minilm_path = os.path.join(os.getcwd(), "models/all-MiniLM-L6-v2/model.onnx")
        minilm_tok = os.path.join(os.getcwd(), "models/all-MiniLM-L6-v2/tokenizer.json")
        minilm = NativeEmbeddingProvider(model_path=minilm_path, tokenizer_path=minilm_tok)
        
        nomic_path = os.path.join(os.getcwd(), "models/nomic-embed-text-v1.5/model.onnx")
        nomic_tok = os.path.join(os.getcwd(), "models/nomic-embed-text-v1.5/tokenizer.json")
        nomic = NativeEmbeddingProvider(model_path=nomic_path, tokenizer_path=nomic_tok)
        
        embedding_manager = EmbeddingManager(default_provider=minilm, default_model_name="dense")
        embedding_manager.register_provider("nomic", nomic)
        
        # 2. Dynamic Qdrant Setup
        vector_store = QdrantVectorStore(client=q_client, embedding_dim=384, vector_name="dense")
        await vector_store.setup()
        # Ensure nomic space exists
        await vector_store.update_collection_schema({"nomic": 768})
        
        # 3. Hybrid Search with Multi-Vector support
        strategies = {
            "fulltext": FullTextStrategy(memory_storage=storage),
            "vector_dense": VectorSearchStrategy(vector_store=vector_store, embedding_provider=minilm, vector_name="dense"),
            "vector_nomic": VectorSearchStrategy(vector_store=vector_store, embedding_provider=nomic, vector_name="nomic")
        }
        
        search_engine = HybridSearchEngine(
            strategies=strategies, 
            embedding_provider=embedding_manager, 
            memory_storage=storage
        )
        
        self.engine = RAEEngine(
            memory_storage=storage, 
            vector_store=vector_store, 
            embedding_provider=embedding_manager,
            llm_provider=None, 
            settings=Settings(), 
            search_engine=search_engine
        )
        
        print(f"🚀 Silicon Oracle 300.10 (Multi-Vector) | Project: {self.agent_id}")

    async def run(self, no_wipe: bool = False):
        with open(self.dataset_path, "r") as f:
            data = yaml.safe_load(f)

        if not no_wipe:
            # WIPE ONLY CURRENT TENANT (ISO Isolation)
            print(f"🧹 Wiping data for tenant {self.tenant_id}...")
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM memories WHERE tenant_id = $1;", self.tenant_id)
            
            # OPTIMIZED BATCH INGESTION (Multi-Vector)
            print(f"📥 Ingesting {len(data['memories'])} memories (Multi-Vector)...")
            for mem in data["memories"]:
                content = mem.get("text") or mem.get("content", "")
                nonce = mem.get("metadata", {}).get("nonce", "")
                
                # 1. Store Metadata in Postgres first
                m_id = await self.engine.store_memory(
                    content=content, tenant_id=self.tenant_id, agent_id=self.agent_id,
                    metadata={**mem.get("metadata", {}), "id": mem["id"], "anchor": nonce}, 
                    layer=mem.get("layer", "episodic")
                )
                
                # 2. Generate all embeddings
                # We access the manager directly from the engine
                all_embs = await self.engine.embedding_provider.generate_all_embeddings([content])
                
                # 3. Store all vectors in Qdrant
                # all_embs is {model_name: [vector]}
                embs_to_store = {name: embs[0] for name, embs in all_embs.items() if embs}
                
                await self.engine.vector_store.add_vector(
                    memory_id=m_id,
                    embedding=embs_to_store,
                    tenant_id=self.tenant_id,
                    layer=mem.get("layer", "episodic")
                )
        else:
            print(f"♻️  Using persistent data in DB (Skipping Ingest)...")

        print(f"🔍 Testing {min(self.queries, len(data['queries']))} queries...")
        total_rr = 0.0
        results_count = 0
        
        for i, q in enumerate(data["queries"][:self.queries], 1):
            raw_results = await self.engine.search_memories(
                q["query"], tenant_id=self.tenant_id, agent_id=self.agent_id, top_k=300,
                enable_reranking=args_rerank # Pass the rerank flag
            )
            
            db_ids = [UUID(str(r["id"])) if isinstance(r, dict) else UUID(str(r[0])) for r in raw_results]
            mapped_ids = []
            if db_ids:
                # SYSTEM 300.12: Deep Lineage Recovery
                # We check both metadata->'id' and metadata->'external_id' (used by some loaders)
                full = await self.pool.fetch("""
                    SELECT id, 
                           COALESCE(metadata->>'id', metadata->>'external_id', metadata->>'parent_id') as orig 
                    FROM memories 
                    WHERE id = ANY($1)
                """, db_ids)
                mapping = {str(m["id"]): str(m["orig"]) for m in full if m["orig"]}
                mapped_ids = [mapping.get(str(uid), str(uid)) for uid in db_ids]

            rank = 0
            for idx, rid in enumerate(mapped_ids, 1):
                # Robust comparison (everything to string)
                target_ids = [str(sid) for qid in q["expected_source_ids"] for sid in [qid]]
                if str(rid) in target_ids:
                    rank = idx
                    total_rr += 1.0 / rank
                    break
            
            # DIAGNOSTIC: Why did we miss Rank 1?
            if rank != 1 and raw_results:
                top_hit = raw_results[0]
                top_id = mapped_ids[0] if mapped_ids else "unknown"
                top_content = top_hit.get("content", "N/A")[:100]
                top_audit = top_hit.get("audit_trail", {})
                logger.info("rank_1_diagnostic", 
                            query=q["query"], 
                            top_hit_id=top_id, 
                            top_content=top_content,
                            top_audit=top_audit,
                            expected=q["expected_source_ids"][:3])

            results_count += 1
            if i % 10 == 0:
                print(f"   ✅ Q{i} | Rank: {rank if rank > 0 else 'MISS'}")

        final_mrr = total_rr / results_count if results_count > 0 else 0
        print(f"\n========================================\nMRR: {final_mrr:.4f}\n========================================")

async def main():
    import uuid
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", type=Path, required=True)
    parser.add_argument("--queries", type=int, default=50)
    parser.add_argument("--rerank", action="store_true")
    parser.add_argument("--no-wipe", action="store_true")
    parser.add_argument("--tenant", type=str, default="00000000-0000-0000-0000-000000000000")
    args = parser.parse_args()
    
    # Use provided tenant or default
    suite_tenant = UUID(args.tenant)
    print(f"🛡️ Suite Isolation Active | Tenant: {suite_tenant}")
    
    runner = RAEBenchmarkRunner(args.set, suite_tenant, queries=args.queries)
    try:
        await runner.setup()
        # Pass rerank arg to run
        global args_rerank
        args_rerank = args.rerank
        await runner.run(no_wipe=args.no_wipe)
    finally:
        if runner.pool: await runner.pool.close()

if __name__ == "__main__":
    asyncio.run(main())
