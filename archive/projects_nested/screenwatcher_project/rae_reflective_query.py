import http.client
import json

def query_reflective():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "query_text": "Code Factory Node1 kubus delegation",
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
    print(json.dumps(query_reflective(), indent=2))
