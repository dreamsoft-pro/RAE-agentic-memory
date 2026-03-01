from rae_task_bridge import RAETaskBridge
import json
import http.client

def test_node_as_model():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    body = {
        "tenant_id": "screenwatcher",
        "project": "screenwatcher_project",
        "prompt": "ping",
        "model": "kubus-gpu-01"
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    conn.request("POST", "/v1/agent/execute", json.dumps(body), headers)
    print(conn.getresponse().read().decode("utf-8"))

if __name__ == "__main__":
    test_node_as_model()
