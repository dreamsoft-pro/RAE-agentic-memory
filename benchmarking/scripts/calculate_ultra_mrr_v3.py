import asyncio
import json
import yaml
import time
import httpx

# Configuration
YAML_PATH = "benchmarking/sets/industrial_ultra.yaml"
RAE_API_URL = "http://localhost:8000"
TENANT_ID = "00000000-0000-0000-0000-000000000999"

async def calculate_mrr():
    print(f"🚀 Starting V3 ACCURATE MRR Calculation for Industrial Ultra (100k)")
    
    # 1. Load ONLY queries from YAML (to save memory and avoid content mapping)
    print(f"📂 Loading queries from {YAML_PATH}...")
    queries = []
    in_queries = False
    with open(YAML_PATH, "r") as f:
        # Simple manual parser to get only the queries section
        all_content = f.read()
        if "queries:" in all_content:
            queries_part = all_content.split("queries:")[1]
            data = yaml.safe_load("queries:" + queries_part)
            queries = data.get('queries', [])
    
    print(f"Loaded {len(queries)} evaluation queries.")

    # 2. Run Queries against API
    reciprocal_ranks = []
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for i, q in enumerate(queries):
            query_text = q['query']
            expected_ids = set(q['expected_source_ids']) # IDs like 'log_00001'
            
            try:
                resp = await client.post(
                    f"{RAE_API_URL}/v1/memory/query",
                    json={"query_text": query_text, "k": 10},
                    headers={"X-Tenant-Id": TENANT_ID}
                )
                
                if resp.status_code == 200:
                    results = resp.json().get('results', [])
                    
                    rank = None
                    for idx, res in enumerate(results, 1):
                        # Our ultra_light backfill stored the YAML ID in 'source'
                        # RAE-Dev API returns 'source' in the result dictionary
                        actual_source_id = res.get('source')
                        
                        if actual_source_id in expected_ids:
                            rank = idx
                            break
                    
                    rr = 1.0 / rank if rank else 0.0
                    reciprocal_ranks.append(rr)
                else:
                    reciprocal_ranks.append(0.0)

                if (i+1) % 10 == 0:
                    print(f"  Query {i+1}/{len(queries)}: MRR so far: {sum(reciprocal_ranks)/len(reciprocal_ranks):.4f}")

            except Exception as e:
                print(f"Error: {e}")
                reciprocal_ranks.append(0.0)

    final_mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0
    print(f"\n✨ Final MRR @10 (100k Scale): {final_mrr:.4f}")

if __name__ == "__main__":
    asyncio.run(calculate_mrr())
