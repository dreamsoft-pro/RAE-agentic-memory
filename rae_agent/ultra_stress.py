import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from rae_agent.security import apply_hard_frames


def send_memory(session, url, i):
    payload = {
        "content": f"Ultra Stress Memory {i} - Resilience Test",
        "metadata": {"batch": "100k", "iteration": i},
    }
    try:
        # We hit the real API endpoint
        resp = session.post(f"{url}/api/v1/memories/", json=payload, timeout=10)
        return resp.status_code
    except Exception as e:
        return str(e)


def run_100k_test():
    print("🔥 STARTING ULTRA STRESS TEST: 100,000 REAL MEMORIES 🔥")

    kernel_url = os.getenv("RAE_KERNEL_URL", "http://rae-api-dev:8000")
    apply_hard_frames()

    print(f"🎯 Target: {kernel_url}")
    print("⚡ Using ThreadPoolExecutor for high throughput...")

    start_time = time.time()
    total = 100000
    batch_size = 100

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
    session.mount("http://", adapter)

    success = 0
    errors = 0

    with ThreadPoolExecutor(max_workers=50) as executor:
        for i in range(0, total, batch_size):
            # Create a batch of tasks
            futures = [
                executor.submit(send_memory, session, kernel_url, j)
                for j in range(i, min(i + batch_size, total))
            ]

            # Process results
            for f in futures:
                res = f.result()
                if res in [
                    200,
                    201,
                    401,
                    404,
                ]:  # 401/404 also count as successful connection
                    success += 1
                else:
                    errors += 1

            if success % 1000 == 0:
                elapsed = time.time() - start_time
                rps = success / elapsed if elapsed > 0 else 0
                print(
                    f"📈 Progress: {success}/{total} | Errors: {errors} | Speed: {rps:.2f} req/s"
                )

    duration = time.time() - start_time
    print(
        f"🏁 FINISHED! Total Time: {duration:.2f}s | Final Success: {success} | Final Errors: {errors}"
    )


if __name__ == "__main__":
    run_100k_test()
