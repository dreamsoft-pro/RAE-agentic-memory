import http.client
import json

def list_reflections():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "tenant_id": "screenwatcher",
        "project": "screenwatcher_project",
        "k": 10
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v1/reflections/query", json.dumps(payload), headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    print(json.dumps(list_reflections(), indent=2))
