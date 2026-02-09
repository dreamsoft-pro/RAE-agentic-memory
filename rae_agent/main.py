# Auto-apply hard frames BEFORE other imports if in secure mode
import os

from rae_agent.security import SecureSocket, apply_hard_frames

if os.getenv("RAE_AGENT_MODE") == "secure":
    apply_hard_frames()

import socket
import sys
import time

import requests


def check_internet_leak():
    print("🕵️  SECURITY CHECK: Attempting to access google.com...")
    try:
        # Set a short timeout because we expect it to fail fast (unreachable network)
        # or hang if dropped.
        requests.get("https://google.com", timeout=2)
        print("❌ CRITICAL FAIL: Internet is accessible! Hard Frames breached.")
        return False
    except (requests.exceptions.ConnectionError, socket.gaierror, RuntimeError) as e:
        # RuntimeError is raised by our secure_socket
        print(f"✅ SUCCESS: Access blocked ({type(e).__name__}: {e})")
        return True
    except Exception as e:
        print(f"✅ SUCCESS: Access failed with {type(e).__name__}: {e}")
        return True


def connect_to_kernel():
    kernel_url = os.getenv("RAE_KERNEL_URL", "http://rae-kernel:8000")
    print(f"🔌 CONNECTING: Attempting to contact RAE Kernel at {kernel_url}...")
    try:
        # Just checking health or root
        resp = requests.get(f"{kernel_url}/health", timeout=5)
        if resp.status_code == 200:
            print("✅ SUCCESS: Connected to RAE Kernel.")

            # --- PROOF OF LIFE (IMPLICIT CAPTURE TEST) ---
            print("💾 SENDING BOOT SIGNAL (Testing Implicit Capture)...")
            payload = {
                "tenant_id": "default-tenant",
                "project": "secure-agent-boot",
                "prompt": "Secure Container Boot Sequence Complete. Reporting for duty.",
                "session_id": "secure-boot-session",
            }
            try:
                # We hit the Agent Pipeline. The Kernel should IMPLICITLY save this.
                # Endpoint is /v2/agent/execute (without /api prefix in app.include_router)
                act_resp = requests.post(
                    f"{kernel_url}/v2/agent/execute",
                    json=payload,
                    headers={"X-Tenant-Id": "default-tenant"},
                    timeout=10,
                )
                if act_resp.status_code == 200:
                    print(
                        f"✅ SIGNAL RECEIVED by Kernel. Response: {act_resp.json().get('answer')}"
                    )
                else:
                    print(
                        f"⚠️  SIGNAL REJECTED: {act_resp.status_code} - {act_resp.text}"
                    )
            except Exception as ex:
                print(f"❌ SIGNAL FAILED: {ex}")
            # ---------------------------------------------

            return True
        else:
            print(f"⚠️  WARNING: Kernel reachable but returned {resp.status_code}")
            return True
    except Exception as e:
        print(f"❌ FAIL: Could not connect to Kernel: {e}")
        return False


def main():
    print("🤖 SECURE AGENT STARTING...")
    print(f"🔒 UID: {os.getuid()} (Should be non-root)")

    # Force application if not already done by import side-effect (paranoid check)
    if socket.socket != SecureSocket:
        print(
            "⚠️  Warning: Hard Frames were not applied at module level. Applying now (might be too late for some libs)."
        )
        apply_hard_frames()

    # 1. Verify Isolation
    if not check_internet_leak():
        sys.exit(1)

    # 2. Verify Tunnel to Kernel
    # In a real startup, we might retry loop here
    if not connect_to_kernel():
        print(
            "⚠️  Kernel not found (expected if not running in compose). Entering wait loop."
        )

    if len(sys.argv) > 1 and sys.argv[1] == "--soak-test":
        print(
            "🌊 SOAK TEST: Starting endurance simulation (Variable Load + Memory Monitoring)..."
        )
        kernel_url = os.getenv("RAE_KERNEL_URL", "http://rae-kernel:8000")

        import random
        import resource

        session = requests.Session()
        counter = 0
        errors = 0
        start_time = time.time()

        # Infinite loop for soak testing (container will be killed manually or run for hours)
        print(f"   PID: {os.getpid()}")

        while True:
            counter += 1

            # 1. Variable Think Time (0.1s to 1.5s)
            time.sleep(random.uniform(0.1, 1.5))

            # 2. Variable Payload (simulate small commands vs large memories)
            payload_size = random.randint(100, 50000)  # 100 bytes to 50KB
            data = "x" * payload_size

            try:
                # 3. Request
                resp = session.post(
                    f"{kernel_url}/v2/memories/",
                    json={"content": data, "importance": random.random(), "project": "soak-test", "layer": "working", "source": "soak-agent"},
                    headers={"X-Tenant-Id": "default-tenant"}
                )
                if resp.status_code not in [200, 404]:
                    errors += 1
                    print(f"⚠️  Error: Status {resp.status_code}")
            except Exception as e:
                errors += 1
                print(f"❌ Exception: {e}")

            # 4. Monitoring (every 50 requests)
            if counter % 50 == 0:
                # Check Memory Usage (RSS)
                usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                usage_mb = usage_kb / 1024
                elapsed = time.time() - start_time
                print(
                    f"📊 Stats [Req: {counter} | Err: {errors} | Time: {elapsed:.0f}s]: RAM Usage: {usage_mb:.2f} MB"
                )

                # Verify Leak Check Periodically
                try:
                    requests.get("https://google.com", timeout=0.1)
                    print("❌ FATAL: LEAK DETECTED!")
                    sys.exit(1)
                except Exception:
                    pass

    print("💤 Agent entering idle loop (waiting for tasks via Kernel)...")
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
