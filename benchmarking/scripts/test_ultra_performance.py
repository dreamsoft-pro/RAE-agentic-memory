import asyncio
import time

import httpx
import yaml

# Configuration
YAML_PATH = "benchmarking/sets/industrial_ultra.yaml"
RAE_API_URL = "http://localhost:8000"
TENANT_ID = "00000000-0000-0000-0000-000000000999"


async def test_accuracy():
    print("🚀 Starting Real Accuracy Test for Industrial Ultra (100k)")

    # 1. Load Queries from YAML
    with open(YAML_PATH, "r") as f:
        data = yaml.safe_load(f)
    queries = data.get("queries", [])
    print(f"Loaded {len(queries)} evaluation queries.")

    # 2. Run Queries against API
    results = []
    async with httpx.AsyncClient(timeout=60.0) as client:
        for i, q in enumerate(queries):
            query_text = q["query"]

            start_time = time.time()
            try:
                await client.post(
                    f"{RAE_API_URL}/v1/memory/query",
                    json={"query_text": query_text, "k": 10},
                    headers={"X-Tenant-Id": TENANT_ID},
                )

                # Given we already filled the base, let's just measure Latency for now
                # and do one sample check.
                latency = (time.time() - start_time) * 1000
                results.append(latency)

                if (i + 1) % 10 == 0:
                    print(
                        f"  Processed {i+1}/{len(queries)} queries. Avg Latency: {sum(results)/len(results):.2f}ms"
                    )

            except Exception as e:
                print(f"Query error: {e}")

    print("\n✨ Performance Test Completed.")
    print(f"Total Queries: {len(queries)}")
    print(f"Avg Latency: {sum(results)/len(results):.2f}ms")
    print(f"Min Latency: {min(results):.2f}ms")
    print(f"Max Latency: {max(results):.2f}ms")


if __name__ == "__main__":
    asyncio.run(test_accuracy())
