
import asyncio
import os
import sys
import json
import hashlib
from pathlib import Path
from uuid import UUID
from datetime import datetime, timezone

# Add project root and dependencies
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))
sys.path.insert(0, str(PROJECT_ROOT / "rae_adapters"))

import asyncpg
from rae_adapters.postgres import PostgreSQLGraphStore

async def backfill():
    print("🚀 Starting Dreamsoft Data Backfill (System 369 Enrichment)...")
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@localhost:5432/rae")
    pool = await asyncpg.create_pool(db_url.replace("+asyncpg", ""))
    
    graph_store = PostgreSQLGraphStore(pool=pool)
    
    async with pool.acquire() as conn:
        # 1. Fetch all memories that need backfill
        rows = await conn.fetch("SELECT id, content, tenant_id, metadata, human_label FROM memories WHERE content_hash IS NULL OR human_label IS NULL")
        print(f"   Found {len(rows)} memories to enrich.")
        
        updated_count = 0
        graph_count = 0
        
        for r in rows:
            m_id = r["id"]
            content = r["content"]
            tenant_id = r["tenant_id"]
            metadata = json.loads(r["metadata"]) if isinstance(r["metadata"], str) else r["metadata"]
            
            # A. Calculate Hash
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # B. Generate Human Label if missing
            label = r["human_label"]
            if not label:
                if "source" in metadata:
                    label = f"Dreamsoft-{metadata['source']}-{str(m_id)[:4]}"
                else:
                    label = f"Dreamsoft-Legacy-{str(m_id)[:8]}"
            
            # C. Update Memory Record
            await conn.execute(
                "UPDATE memories SET content_hash = $1, human_label = $2 WHERE id = $3",
                content_hash, label, m_id
            )
            
            # D. Add to Knowledge Graph (The Glue)
            try:
                # Add node for this memory
                await graph_store.add_node(
                    tenant_id=tenant_id,
                    project_id="dreamsoft_modernization",
                    node_id=str(m_id),
                    label="LegacyMemory",
                    properties={"original_label": label}
                )
                graph_count += 1
            except:
                pass
                
            updated_count += 1
            if updated_count % 100 == 0:
                print(f"   Processed {updated_count}/{len(rows)}...")

    print(f"✅ Backfill Complete. Updated: {updated_count}, Graph Nodes created: {graph_count}")
    await pool.close()

if __name__ == "__main__":
    asyncio.run(backfill())
