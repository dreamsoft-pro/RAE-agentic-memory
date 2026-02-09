import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

# Ensure we can import from project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    from rae_agent.security import apply_hard_frames
except ImportError:
    print("⚠️ 'rae_agent.security' not found. Hard Frames mode might be incomplete.")
    def apply_hard_frames():
        return None

def send_single_memory(session, url, memory, api_key, tenant_id):
    # Map 'text' to 'content' for API compatibility
    if "text" in memory and "content" not in memory:
        memory["content"] = memory.pop("text")

    # Ensure project is set
    if "project" not in memory:
        memory["project"] = "industrial_ultra_200q"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Tenant-Id": tenant_id,
    }
    try:
        resp = session.post(url, json=memory, headers=headers, timeout=30)
        if resp.status_code not in [200, 201]:
            return f"Error {resp.status_code}: {resp.text[:200]}"
        return "OK"
    except Exception as e:
        return str(e)

def ingest_batches(memories, batch_size=500):
    print(f"🚀 Starting ingestion of {len(memories)} memories in batches of {batch_size}...")

    # Use localhost:8001 (Lite/Dev port) or user env
    base_url = os.getenv("RAE_KERNEL_URL", "http://localhost:8001")
    target_url = f"{base_url}/v2/memories/"
    api_key = os.getenv("RAE_API_KEY", "dev-key")
    tenant_id = os.getenv("RAE_TENANT_ID", "00000000-0000-0000-0000-000000000000")

    apply_hard_frames()

    session = requests.Session()
    # Moderate pool size for older hardware
    adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
    session.mount("http://", adapter)

    total = len(memories)
    processed = 0
    errors = 0

    for i in range(0, total, batch_size):
        batch = memories[i:i+batch_size]
        print(f"📦 Processing batch {i//batch_size + 1}/{(total//batch_size)+1} ({len(batch)} items)...")

        # Use low concurrency (5 workers) to prevent laptop overload
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(send_single_memory, session, target_url, m, api_key, tenant_id)
                for m in batch
            ]

            for f in as_completed(futures):
                res = f.result()
                if res != "OK":
                    errors += 1
                    # Only print first few errors to avoid spam
                    if errors <= 10:
                        print(f"❌ Error: {res}")

        processed += len(batch)
        print(f"✅ Batch complete. Progress: {processed}/{total}. Total Errors: {errors}")

        # Small cooldown for the "old laptop"
        time.sleep(0.2)

def prepare():
    ultra_path = Path("benchmarking/sets/industrial_ultra.yaml")
    extreme_path = Path("benchmarking/sets/industrial_extreme.yaml")
    output_path = Path("benchmarking/sets/industrial_ultra_200q.yaml")

    try:
        from yaml import CSafeLoader as Loader
    except ImportError:
        from yaml import SafeLoader as Loader

    print(f"📖 Reading {ultra_path} (this may take a minute)...")
    start_read = time.time()
    with open(ultra_path, "r") as f:
        ultra_data = yaml.load(f, Loader=Loader)
    print(f"✅ Read {ultra_path} in {time.time() - start_read:.2f}s")

    print(f"📖 Reading queries from {extreme_path}...")
    with open(extreme_path, "r") as f:
        extreme_data = yaml.load(f, Loader=Loader)

    # Replace ultra queries with extreme queries (which has 200)
    ultra_data["queries"] = extreme_data["queries"]
    ultra_data["name"] = "industrial_ultra_200q"
    ultra_data["description"] = "Industrial Ultra (100k) with 200 queries for Bandit convergence"

    # Ingest memories if present
    if "memories" in ultra_data:
        ingest_batches(ultra_data["memories"], batch_size=500)
    else:
        print("⚠️ No 'memories' list found in industrial_ultra.yaml!")

    print(f"💾 Saving dataset config to {output_path}...")
    with open(output_path, "w") as f:
        yaml.safe_dump(ultra_data, f)

    print("✅ Done!")

if __name__ == "__main__":
    prepare()
