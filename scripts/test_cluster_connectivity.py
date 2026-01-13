import subprocess
import requests
import json
import time

# Konfiguracja (zgodna z wiedzą operacyjną)
NODE1_IP = "100.68.166.117"
NODE1_USER = "operator"
NODE3_IP = "172.30.15.11"
NODE3_PORT = 11434

def test_node1_ssh():
    print(f"\n🖥️  Testing Node1 (Code Factory) via SSH [{NODE1_IP}]...")
    cmd = [
        "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
        f"{NODE1_USER}@{NODE1_IP}",
        "uname -a && python3 -c 'print(\"✅ Node1 Python Execution Works!\")'"
    ]
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Success ({duration:.2f}s):")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed (Return Code {result.returncode}):")
            print(f"   Stderr: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_node3_inference():
    print(f"\n🧠 Testing Node3 (Inference) via VPN [{NODE3_IP}]...")
    url = f"http://{NODE3_IP}:{NODE3_PORT}/api/generate"
    payload = {
        "model": "llama3.1:8b",
        "prompt": "Say exactly: 'Node3 Inference Online'",
        "stream": False
    }
    
    try:
        start_time = time.time()
        res = requests.post(url, json=payload, timeout=10)
        duration = time.time() - start_time
        
        if res.status_code == 200:
            response_text = res.json().get("response", "").strip()
            print(f"✅ Success ({duration:.2f}s):")
            print(f"   Model Response: '{response_text}'")
            return True
        else:
            print(f"❌ Failed (Status {res.status_code}): {res.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Cluster Connectivity Test...")
    n1 = test_node1_ssh()
    n3 = test_node3_inference()
    
    if n1 and n3:
        print("\n🎉 ALL SYSTEMS GO: Cluster is fully operational.")
        exit(0)
    else:
        print("\n⚠️ PARTIAL FAILURE: Check logs above.")
        exit(1)
