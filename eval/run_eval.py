import yaml, requests, os, statistics, time

API = os.environ.get("MEMORY_API_URL", "http://localhost:8000")

def main():
    with open("eval/goldenset.yaml", "r", encoding="utf-8") as f:
        gs = yaml.safe_load(f)
    latencies = []
    hits = []
    for q in gs.get("queries", []):
        t0 = time.time()
        r = requests.post(f"{API}/memory/query", json={
            "tenant_id": "eval-tenant",
            "query_text": q["query"],
            "k": 50, "k_final": 5
        }, headers={"X-Tenant-Id": "eval-tenant"})
        dt = (time.time() - t0) * 1000
        latencies.append(dt)
        data = r.json()
        expected = set(q.get("expected_source_ids", []))
        got = {item.get("source_id") for item in data.get("results", []) if item.get("source_id")}
        hits.append(1 if expected & got else 0)
    p95 = sorted(latencies)[int(0.95*len(latencies))-1] if latencies else 0
    print({"hit_rate@5": sum(hits)/len(hits) if hits else 0, "p95_ms": p95})

if __name__ == "__main__":
    main()
