import http.client
import json

def search_no_project():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": None,
        "query_text": "SECRET_KEY_FOR_NODE1",
        "limit": 5
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
    print(json.dumps(search_no_project(), indent=2))
