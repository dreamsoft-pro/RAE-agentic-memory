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
sys.path.insert(0, str(PROJECT_ROOT / "rae_adapters"))

from rae_adapters.postgres import PostgreSQLStorage, PostgreSQLGraphStore
from rae_adapters.qdrant import QdrantVectorStore
from rae_core.embedding.native import NativeEmbeddingProvider
from rae_core.engine import RAEEngine
from rae_core.config.settings import RAESettings as Settings
from rae_core.search.engine import HybridSearchEngine
from rae_core.search.strategies.vector import VectorSearchStrategy
from rae_core.search.strategies.fulltext import FullTextStrategy
from rae_core.embedding.manager import EmbeddingManager

logger = structlog.get_logger(__name__)

class RAEBenchmarkRunner:
    def __init__(self, dataset_path: str, tenant_id: UUID, queries: int = 50):
        self.dataset_path = Path(dataset_path)
        self.tenant_id = tenant_id
        self.queries = queries
        self.agent_id = self.dataset_path.stem
        self.pool = None

    async def setup(self):
        import asyncpg
        from qdrant_client import AsyncQdrantClient
        
        db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@localhost/rae")
        self.pool = await asyncpg.create_pool(db_url.replace("+asyncpg", ""))
        
        q_client = AsyncQdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)
        storage = PostgreSQLStorage(pool=self.pool)
        self.graph_store = PostgreSQLGraphStore(pool=self.pool)
        
        # 1. Initialize Multiple Models
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
        await vector_store.update_collection_schema({"nomic": 768})
        
        # 3. Hybrid Search
        strategies = {
            "fulltext": FullTextStrategy(memory_storage=storage),
            "vector_dense": VectorSearchStrategy(vector_store=vector_store, embedding_provider=minilm, vector_name="dense"),
            "vector_nomic": VectorSearchStrategy(vector_store=vector_store, embedding_provider=nomic, vector_name="nomic")
        }
        
        # Restore MRR 1.0 Weights (Math-First)
        self.strategy_weights = {"fulltext": 100.0, "vector_dense": 1.0, "vector_nomic": 1.0}
        
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
            search_engine=search_engine,
            graph_store=self.graph_store
        )
        
        print(f"🚀 Silicon Oracle 300.11 (Multi-Vector + Graph) | Project: {self.agent_id}")

    async def run(self, no_wipe: bool = False):
        with open(self.dataset_path, "r") as f:
            data = yaml.safe_load(f)

        if not no_wipe:
            print(f"🧹 Wiping data for tenant {self.tenant_id}...")
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM memories WHERE tenant_id = $1;", self.tenant_id)
                await conn.execute("DELETE FROM knowledge_graph_nodes WHERE tenant_id = $1;", self.tenant_id)
                await conn.execute("DELETE FROM knowledge_graph_edges WHERE tenant_id = $1;", self.tenant_id)
            
            print(f"📥 Ingesting {len(data['memories'])} memories...")
            for mem in data["memories"]:
                content = mem.get("text") or mem.get("content", "")
                nonce = mem.get("metadata", {}).get("nonce", "")
                
                # Full universal_ingest via store_memory
                await self.engine.store_memory(
                    content=content, tenant_id=self.tenant_id, agent_id=self.agent_id,
                    metadata={**mem.get("metadata", {}), "id": mem["id"], "anchor": nonce}, 
                    layer=mem.get("layer", "episodic")
                )
        else:
            print(f"♻️  Using persistent data in DB...")

        print(f"🔍 Testing {min(self.queries, len(data['queries']))} queries...")
        total_rr = 0.0
        results_count = 0
        
        for i, q in enumerate(data["queries"][:self.queries], 1):
            raw_results = await self.engine.search_memories(
                q["query"], tenant_id=self.tenant_id, agent_id=self.agent_id, top_k=10,
                enable_reranking=False,
                strategy_weights=self.strategy_weights
            )
            
            db_ids = [UUID(str(r["id"])) if isinstance(r, dict) else UUID(str(r[0])) for r in raw_results]
            mapped_ids = []
            if db_ids:
                full = await self.pool.fetch("""
                    SELECT id, COALESCE(metadata->>'id', metadata->>'external_id', metadata->>'parent_id') as orig 
                    FROM memories WHERE id = ANY($1)""", db_ids)
                id_map = {r["id"]: r["orig"] for r in full}
                mapped_ids = [id_map.get(db_id) for db_id in db_ids]

            rank = 0
            expected = q.get("expected_source_ids", q.get("expected", []))
            for idx, m_id in enumerate(mapped_ids, 1):
                if m_id in expected:
                    rank = idx
                    break
            
            rr = 1.0 / rank if rank > 0 else 0
            total_rr += rr
            results_count += 1
            
            if i % 10 == 0 or rank != 1:
                print(f"   Q{i:3} | Rank: {rank if rank > 0 else 'MISS'}")

        final_mrr = total_rr / results_count if results_count > 0 else 0
        print(f"\n========================================\nMRR: {final_mrr:.4f}\n========================================")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", required=True)
    parser.add_argument("--queries", type=int, default=50)
    parser.add_argument("--rerank", action="store_true")
    parser.add_argument("--no-wipe", action="store_true")
    parser.add_argument("--tenant", type=str, default="00000000-0000-0000-0000-000000000000")
    args = parser.parse_args()
    
    suite_tenant = UUID(args.tenant)
    print(f"🛡️ Suite Isolation Active | Tenant: {suite_tenant}")
    
    runner = RAEBenchmarkRunner(args.set, suite_tenant, queries=args.queries)
    try:
        await runner.setup()
        await runner.run(no_wipe=args.no_wipe)
    finally:
        if runner.pool: await runner.pool.close()

if __name__ == "__main__":
    asyncio.run(main())
