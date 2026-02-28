import http.client
import json

def search_node_specs():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "query_text": "task type definition for compute nodes control plane supported actions",
        "limit": 20
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v1/memory/query", json.dumps(payload), headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    result = search_node_specs()
    print(json.dumps(result, indent=2))
