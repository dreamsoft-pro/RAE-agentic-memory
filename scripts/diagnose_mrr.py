import asyncio
import os
import structlog
import json
from rae_core.math.logic_gateway import LogicGateway
from rae_adapters.postgres import PostgreSQLStorage
from rae_core.search.strategies.fulltext import FullTextStrategy

async def diagnose():
    # Setup
    dsn = "postgresql://rae:rae_password@localhost:5432/rae"
    storage = PostgreSQLStorage(dsn=dsn)
    
    # LogicGateway (System 4.16)
    gateway = LogicGateway()
    gateway.storage = storage
    
    # Query from benchmark
    query = "Are there any critical payment system problems?"
    tenant_id = "00000000-0000-0000-0000-000000000000"
    project_id = "industrial_small"
    
    print(f"\n--- DIAGNOSING QUERY: {query} ---")
    
    # 1. Fetch FTS results
    fts_strategy = FullTextStrategy(storage)
    fts_results = await fts_strategy.search(query, tenant_id, limit=50, agent_id=project_id)
    
    if not fts_results:
        print("❌ NO FTS RESULTS FOUND!")
        return

    print(f"\nFTS RAW RESULTS (Top 5):")
    processed_results = []
    for i, res in enumerate(fts_results[:5], 1):
        m_id = res[0] if isinstance(res, tuple) else res.id
        score = res[1] if isinstance(res, tuple) else res.score
        
        mem = await storage.get_memory(m_id, tenant_id)
        if mem:
            print(f"{i}. [FTS Score: {score:.2f}] ID: {m_id}")
            print(f"   Content: {mem['content'][:100]}...")
        else:
            print(f"{i}. ID: {m_id} NOT FOUND IN DB!")
        
    for res in fts_results:
        m_id = res[0] if isinstance(res, tuple) else res.id
        score = res[1] if isinstance(res, tuple) else res.score
        importance = res[2] if isinstance(res, tuple) and len(res) > 2 else 0.0
        processed_results.append((m_id, score, importance))

    # 2. Manual Fusion & Rerank via LogicGateway
    strategy_results = {"fulltext": processed_results, "vector": []}
    
    # Batch fetch contents for gateway
    all_ids = [r[0] for r in processed_results]
    mems = await storage.get_memories_batch(all_ids, tenant_id)
    memory_contents = {m["id"]: m for m in mems}
    
    fused = await gateway.fuse(
        strategy_results=strategy_results,
        weights={"fulltext": 10.0, "vector": 0.5},
        query=query,
        memory_contents=memory_contents
    )
    
    print(f"\nFUSED & RERANKED RESULTS (Top 5):")
    for i, res in enumerate(fused[:5], 1):
        m_id = res[0]
        score = res[1]
        mem = memory_contents.get(m_id, {})
        content = mem.get("content", "N/A")
        print(f"{i}. [Final Score: {score:.2e}] ID: {m_id}")
        print(f"   Content: {content[:200]}...")
        print(f"   Metadata: {mem.get('metadata', {})}")

if __name__ == "__main__":
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["QDRANT_HOST"] = "localhost"
    asyncio.run(diagnose())