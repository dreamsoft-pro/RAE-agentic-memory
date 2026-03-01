import http.client
import json

def search_start_cmd():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": None,
        "query_text": "python rae_worker start command compute node",
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
    print(json.dumps(search_start_cmd(), indent=2))
