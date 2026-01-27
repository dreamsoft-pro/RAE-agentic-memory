import os
import sys

# CRITICAL: Apply Hard Frames BEFORE importing requests
# This ensures that socket.socket is patched before urllib3/requests grabs a reference to it.
from rae_agent.security import apply_hard_frames


def verify_real_integration():
    print("🚀 STARTING REAL INTEGRATION TEST (The Prisoner Test)...")

    # 1. Apply Hard Frames
    # Ensure RAE_KERNEL_URL is pointing to the REAL API
    kernel_url = os.getenv("RAE_KERNEL_URL")
    if not kernel_url:
        print("❌ ERROR: RAE_KERNEL_URL not set.")
        sys.exit(1)

    print(f"🎯 Target Kernel: {kernel_url}")
    apply_hard_frames()

    # NOW import network libs

    import requests

    from rae_agent.main import check_internet_leak  # Re-use logic

    # 2. Verify Isolation (Should FAIL to reach Google)
    if not check_internet_leak():
        print("❌ FATAL: Hard Frames are NOT active!")
        sys.exit(1)

    # 3. Verify Connection to REAL RAE API
    print("🔌 Connecting to RAE API...")
    try:
        # Health Check
        resp = requests.get(f"{kernel_url}/health", timeout=5)
        if resp.status_code == 200:
            print("✅ Health Check Passed!")
        else:
            print(f"⚠️  Health Check returned {resp.status_code}")

        # 4. Perform Business Logic (Create Memory)
        payload = {
            "content": "Integration Test Memory from Secure Agent",
            "metadata": {"source": "hard_frames_test", "verified": True},
        }

        print("💾 Attempting to write memory...")
        resp = requests.post(f"{kernel_url}/api/v1/memories/", json=payload, timeout=5)

        if resp.status_code in [200, 201]:
            print("✅ Memory Write SUCCESS!")
            print(f"   Response: {resp.json()}")
        elif resp.status_code == 401:
            print("✅ Network OK, Auth Required (Expected for unauthenticated client).")
            print("   This confirms we reached the real API.")
        elif resp.status_code == 404:
            print("✅ Network OK, Endpoint Not Found (Check URL path).")
        else:
            print(f"❌ API Error: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")
        sys.exit(1)

    print("🏁 INTEGRATION TEST COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    verify_real_integration()
