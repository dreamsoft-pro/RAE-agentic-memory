import http.client
import json

def global_search(query):
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    # Search without project to find system-wide context
    payload = {
        "project": None, 
        "query_text": query,
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
    print(json.dumps(global_search("kubus-gpu-01"), indent=2))
    print(json.dumps(global_search("Node1"), indent=2))
