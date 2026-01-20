import os
import sys
import time
import requests
import socket

# --- HARD FRAME: PROTOCOL EXCLUSIVITY (Phase 2.1) ---
_real_socket = socket.socket
_kernel_host = os.getenv("RAE_KERNEL_URL", "172.29.99.2").split("//")[-1].split(":")[0]

def secure_socket(*args, **kwargs):
    # This is a very basic example of a semantic socket gate
    # In production, this would be more robust.
    caller_frame = sys._getframe(1)
    # Check if we are being called by 'requests' or internal library
    # For this test, we just throw if it's not our allowed host
    s = _real_socket(*args, **kwargs)
    
    _orig_connect = s.connect
    def gated_connect(address):
        host = address[0]
        if host != _kernel_host and host != "127.0.0.1":
            raise RuntimeError(f"Use RAE Protocol. Connection to {host} denied.")
        return _orig_connect(address)
    
    s.connect = gated_connect
    return s

# Apply the patch
socket.socket = secure_socket
# ----------------------------------------------------

def check_internet_leak():
    print("🕵️  SECURITY CHECK: Attempting to access google.com...")
    try:
        # Set a short timeout because we expect it to fail fast (unreachable network)
        # or hang if dropped.
        requests.get("https://google.com", timeout=2)
        print("❌ CRITICAL FAIL: Internet is accessible! Hard Frames breached.")
        return False
    except (requests.exceptions.ConnectionError, socket.gaierror):
        print("✅ SUCCESS: Internet is unreachable.")
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
    
    # 1. Verify Isolation
    if not check_internet_leak():
        sys.exit(1)
        
    # 2. Verify Tunnel to Kernel
    # In a real startup, we might retry loop here
    if not connect_to_kernel():
        print("⚠️  Kernel not found (expected if not running in compose). Entering wait loop.")
    
    print("💤 Agent entering idle loop (waiting for tasks via Kernel)...")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
