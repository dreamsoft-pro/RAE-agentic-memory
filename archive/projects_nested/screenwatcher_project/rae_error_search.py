import http.client
import json

def search_error():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": None,
        "query_text": "unknown_task_type solution node1 kubus",
        "limit": 20
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v2/memories/query", json.dumps(payload), headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    result = search_error()
    print(json.dumps(result, indent=2))
