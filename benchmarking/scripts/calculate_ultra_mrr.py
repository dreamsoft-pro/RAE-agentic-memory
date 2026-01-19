import asyncio

import httpx
import yaml

# Configuration
YAML_PATH = "benchmarking/sets/industrial_ultra.yaml"
RAE_API_URL = "http://localhost:8000"
TENANT_ID = "00000000-0000-0000-0000-000000000999"


async def calculate_mrr():
    print("🚀 Starting ACCURATE MRR Calculation for Industrial Ultra (100k)")

    # 1. Load Queries from YAML
    with open(YAML_PATH, "r") as f:
        data = yaml.safe_load(f)
    queries = data.get("queries", [])
    print(f"Loaded {len(queries)} evaluation queries.")

    # 2. Run Queries against API
    reciprocal_ranks = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        for i, q in enumerate(queries):
            query_text = q["query"]
            expected_ids = set(q["expected_source_ids"])

            try:
                # Use project='ultra_v2' filter if API supports it,
                # or just query and look at 'source' field in results
                resp = await client.post(
                    f"{RAE_API_URL}/v1/memory/query",
                    json={"query_text": query_text, "k": 10},
                    headers={"X-Tenant-Id": TENANT_ID},
                )

                if resp.status_code == 200:
                    results = resp.json().get("results", [])

                    rank = None
                    for idx, res in enumerate(results, 1):
                        # The YAML ID is stored in 'source' (based on our new backfill)
                        yaml_id = res.get("source")

                        if yaml_id in expected_ids:
                            rank = idx
                            break

                    rr = 1.0 / rank if rank else 0.0
                    reciprocal_ranks.append(rr)
                else:
                    reciprocal_ranks.append(0.0)

                if (i + 1) % 10 == 0:
                    print(
                        f"  Query {i+1}/{len(queries)}: MRR so far: {sum(reciprocal_ranks)/len(reciprocal_ranks):.4f}"
                    )

            except Exception as e:
                print(f"Error: {e}")
                reciprocal_ranks.append(0.0)

    final_mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0
    print(f"\n✨ Accurate MRR @10: {final_mrr:.4f}")


if __name__ == "__main__":
    asyncio.run(calculate_mrr())
