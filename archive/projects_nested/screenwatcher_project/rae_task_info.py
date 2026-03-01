import http.client
import json

def query_task_types():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "query_text": "supported task types for node1 kubus-gpu-01",
        "limit": 10
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    conn.request("POST", "/v1/memory/query", json.dumps(payload), headers)
    print(conn.getresponse().read().decode())

if __name__ == "__main__":
    query_task_types()
