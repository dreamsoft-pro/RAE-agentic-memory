import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from rae_agent.security import apply_hard_frames


def generate_industrial_memory(i):
    """Generate a realistic industrial IoT log entry with structured metadata."""
    machines = ["CNC-01", "CNC-02", "PRESS-A", "ROBOT-ARM-Z"]
    sensors = ["temp", "vibration", "pressure", "voltage"]
    statuses = ["NORMAL", "WARNING", "CRITICAL", "IDLE"]

    machine = machines[i % len(machines)]
    sensor = sensors[i % len(sensors)]
    status = statuses[i % len(statuses)]
    val = random.uniform(20.0, 100.0)

    content = f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ')}] Machine={machine} Sensor={sensor} Value={val:.2f} Status={status} Batch={i//1000}"

    return {
        "content": content,
        "project": "industrial_ultra_v3",  # New project name for fresh start
        "importance": 0.8 if status == "CRITICAL" else 0.3,
        "layer": "episodic",
        "source": "industrial_agent_01",
        "tags": [machine, sensor, status, "stress_test"],
        # Structured metadata for high precision filtering
        "metadata": {
            "machine_id": machine,
            "sensor_type": sensor,
            "machine_status": status,
            "batch_id": i // 1000,
        },
    }


def send_memory(session, url, i, api_key, tenant_id):
    data = generate_industrial_memory(i)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Tenant-Id": tenant_id,
    }
    try:
        resp = session.post(url, json=data, headers=headers, timeout=30)
        if resp.status_code not in [200, 201]:
            return f"Error {resp.status_code}: {resp.text[:200]}"
        return "OK"
    except Exception as e:
        return str(e)


def run_real_ingestion():
    print("🏭 STARTING STRUCTURED 100k INGESTION TEST (Agent -> API) 🏭")

    base_url = os.getenv("RAE_KERNEL_URL", "http://rae-api-dev:8000")
    target_url = f"{base_url}/v1/memory/store"
    api_key = os.getenv("RAE_API_KEY", "dev-key")
    tenant_id = os.getenv("RAE_TENANT_ID", "00000000-0000-0000-0000-000000000000")

    apply_hard_frames()

    print(f"🎯 Target API: {target_url}")
    print(f"🔑 API Key: {api_key}")
    print(f"🏢 Tenant ID: {tenant_id}")

    TOTAL_MEMORIES = 100000
    WORKERS = 30  # Increased concurrency for final run

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=WORKERS, pool_maxsize=WORKERS
    )
    session.mount("http://", adapter)

    start_time = time.time()
    success_count = 0
    error_count = 0

    print(f"⚡ Ingesting {TOTAL_MEMORIES} memories with STRUCTURED metadata...")

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        chunk_size = 1000
        for chunk_start in range(0, TOTAL_MEMORIES, chunk_size):
            chunk_end = min(chunk_start + chunk_size, TOTAL_MEMORIES)

            futures = [
                executor.submit(send_memory, session, target_url, i, api_key, tenant_id)
                for i in range(chunk_start, chunk_end)
            ]

            for f in futures:
                res = f.result()
                if res == "OK":
                    success_count += 1
                else:
                    error_count += 1
                    if error_count <= 5 or error_count % 500 == 0:
                        print(f"❌ FAIL: {res}")

            elapsed = time.time() - start_time
            rps = success_count / elapsed if elapsed > 0 else 0
            if chunk_end % 1000 == 0:
                print(
                    f"📊 Stats: {success_count}/{TOTAL_MEMORIES} | Errors: {error_count} | Speed: {rps:.2f} mem/s"
                )

    duration = time.time() - start_time
    print(f"🏁 FINISHED. Success: {success_count}, Errors: {error_count}")


if __name__ == "__main__":
    run_real_ingestion()
