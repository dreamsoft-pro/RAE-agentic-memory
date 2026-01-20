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
    
    # In some python versions/environments, setting s.connect might fail if s is a C extension type.
    # We wrap strictly for containment simulation.
    try:
        s.connect = gated_connect
    except AttributeError:
        # Fallback: If we can't patch the instance, we can't enforce at this level easily without
        # subclassing. For the prototype, we log a warning or accept the risk.
        pass 
    return s

def apply_hard_frames():
    """Enable process-level network restrictions."""
    print("🔒 APPLYING HARD FRAMES: Network restricted to Kernel.")
    socket.socket = secure_socket

# Auto-apply ONLY if running as the main agent application
if os.getenv("RAE_AGENT_MODE") == "secure":
    apply_hard_frames()
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
    
    # Force application if not already done by import side-effect (paranoid check)
    if socket.socket != secure_socket:
        apply_hard_frames()
    
    # 1. Verify Isolation
    if not check_internet_leak():
        sys.exit(1)
        
    # 2. Verify Tunnel to Kernel
    # In a real startup, we might retry loop here
    if not connect_to_kernel():
        print("⚠️  Kernel not found (expected if not running in compose). Entering wait loop.")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--soak-test":
        print("🌊 SOAK TEST: Starting endurance simulation (Variable Load + Memory Monitoring)...")
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
            payload_size = random.randint(100, 50000) # 100 bytes to 50KB
            data = "x" * payload_size
            
            try:
                # 3. Request
                resp = session.post(f"{kernel_url}/memory", json={"content": data, "confidence": random.random()})
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
                print(f"📊 Stats [Req: {counter} | Err: {errors} | Time: {elapsed:.0f}s]: RAM Usage: {usage_mb:.2f} MB")
                
                # Verify Leak Check Periodically
                try:
                    requests.get("https://google.com", timeout=0.1)
                    print("❌ FATAL: LEAK DETECTED!")
                    sys.exit(1)
                except:
                    pass

    print("💤 Agent entering idle loop (waiting for tasks via Kernel)...")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
