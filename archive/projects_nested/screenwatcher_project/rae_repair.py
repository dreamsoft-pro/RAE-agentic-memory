import http.client
import json

def repair_and_check():
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    
    # 1. Try to trigger reflection rebuild
    conn1 = http.client.HTTPConnection("100.66.252.117", 8000)
    print("[*] Triggering RAE database rebuild...")
    payload = {"project": "screenwatcher_project", "tenant_id": "screenwatcher"}
    try:
        conn1.request("POST", "/v2/memories/rebuild-reflections", json.dumps(payload), headers)
        res1 = conn1.getresponse()
        print(f"Rebuild status: {res1.status}")
        print(res1.read().decode())
    except Exception as e:
        print(f"Rebuild failed: {e}")
    finally:
        conn1.close()

    # 2. Get detailed node info
    conn2 = http.client.HTTPConnection("100.66.252.117", 8000)
    print("\n[*] Fetching detailed capabilities...")
    try:
        conn2.request("GET", "/control/nodes", None, headers)
        res2 = conn2.getresponse()
        print(f"Nodes status: {res2.status}")
        print(json.dumps(json.loads(res2.read().decode()), indent=2))
    except Exception as e:
        print(f"Fetch failed: {e}")
    finally:
        conn2.close()

if __name__ == "__main__":
    repair_and_check()

