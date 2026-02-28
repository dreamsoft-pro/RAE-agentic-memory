"""
Generates a benchmark query set based on data already present in the RAE database.
Enables 'DB-First' benchmarking without repeated ingestion.
"""

import asyncio
import os
import sys
import yaml
from pathlib import Path
import structlog

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))

from rae_adapters.postgres import PostgreSQLStorage

async def generate_queries_from_db(project_name: str, num_queries: int = 100):
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@postgres/rae")
    storage = PostgreSQLStorage(db_url)
    
    tenant_id = "00000000-0000-0000-0000-000000000000"
    
    print(f"🔍 Fetching target memories from project {project_name}...")
    memories = await storage.list_memories(tenant_id=tenant_id, limit=2000)
    # Filter by project
    project_mems = [m for m in memories if m.get("project") == project_name]
    
    if not project_mems:
        print(f"❌ No memories found for project {project_name}")
        return

    import random
    targets = random.sample(project_mems, min(num_queries, len(project_mems)))
    
    queries = []
    for m in targets:
        content = m["content"]
        # Extract technical anchors (IDs, Codes) from content
        import re
        anchors = re.findall(r'[A-Z0-9]{2,}-[A-Z0-9-]{3,}', content)
        
        if anchors:
            # Atomic Lookup Query
            anchor = random.choice(anchors)
            query_text = f"Find information related to {anchor}"
        else:
            # Semantic snippet query
            words = content.split()
            query_text = " ".join(words[:min(6, len(words))])

        queries.append({
            "query": query_text,
            "expected_source_ids": [str(m["id"])],
            "category": "industrial_atomic" if anchors else "semantic_prose"
        })

    benchmark = {
        "name": f"gold_db_benchmark_{project_name}",
        "description": f"Benchmark generated from existing data in project {project_name}",
        "queries": queries,
        "config": {
            "top_k": 10,
            "skip_ingestion": True # Custom flag for the runner
        }
    }

    output_path = PROJECT_ROOT / f"benchmarking/sets/gold_db_{project_name.lower()}.yaml"
    with open(output_path, "w") as f:
        yaml.dump(benchmark, f, sort_keys=False)
    
    print(f"✨ Created benchmark set with {len(queries)} queries at {output_path}")

if __name__ == "__main__":
    asyncio.run(generate_queries_from_db("GOLD_SET_1K"))
