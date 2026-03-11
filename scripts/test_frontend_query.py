
import asyncio
import os
import sys
import json
from pathlib import Path
from uuid import UUID, uuid5

# Add project root and dependencies
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))
sys.path.insert(0, str(PROJECT_ROOT / "rae_adapters"))

from rae_core.engine import RAEEngine
from rae_adapters.postgres import PostgreSQLStorage, PostgreSQLGraphStore
from rae_adapters.qdrant import QdrantVectorStore
from rae_core.embedding.native import NativeEmbeddingProvider
import asyncpg
from qdrant_client import AsyncQdrantClient

# Standard RAE Tenant for Frontend
DREAMSOFT_NAMESPACE = UUID("550e8400-e29b-41d4-a716-446655440000")
DREAMSOFT_TENANT = uuid5(DREAMSOFT_NAMESPACE, "DREAMSOFT-FRONTEND-ASSEMBLY")

async def test_frontend_discovery():
    print(f"🔍 Testing RAE Discovery for Frontend (Tenant: {DREAMSOFT_TENANT})...")
    
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@localhost:5432/rae")
    pool = await asyncpg.create_pool(db_url.replace("+asyncpg", ""))
    storage = PostgreSQLStorage(pool=pool)
    graph_store = PostgreSQLGraphStore(pool=pool)
    
    # 1. Search for the Assembly Plan
    print("\n--- [ REFLECTIVE MASTER PLAN ] ---")
    plan = await storage.search_memories(
        query="Frontend Assembly Plan",
        tenant_id=str(DREAMSOFT_TENANT),
        agent_id="Lumina-Architect",
        limit=1
    )
    if plan:
        print(f"Found Plan: {plan[0]['content']}")
        meta = plan[0].get("metadata", {}).get("status", {})
        print(f"Status: {meta.get('status')}")
        print(f"Missing Elements: {', '.join(meta.get('missing_elements', []))}")
    
    # 2. Query Knowledge Graph for Calculation Symbols
    print("\n--- [ GRAPH DISCOVERY: CALCULATION ] ---")
    # We search nodes with label FrontendComponent that contain 'Calculation'
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT node_id, label, properties->>'human_label' as name, properties->>'symbols' as symbols
            FROM knowledge_graph_nodes 
            WHERE tenant_id = $1 AND node_id ILIKE '%Calculation%'
            LIMIT 5
        """, DREAMSOFT_TENANT)
        
        for r in rows:
            print(f"Component: {r['name']} ({r['node_id']})")
            syms = json.loads(r['symbols']) if r['symbols'] else []
            print(f"   Symbols found: {len(syms)} (e.g., {', '.join(syms[:3])}...)")

    await pool.close()

if __name__ == "__main__":
    asyncio.run(test_frontend_discovery())
