import http.client
import json

def list_triggers():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    params = "?tenant_id=screenwatcher&project_id=screenwatcher_project"
    headers = {'X-Tenant-Id': 'screenwatcher'}
    try:
        conn.request("GET", f"/v1/triggers/list{params}", headers=headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    print(json.dumps(list_triggers(), indent=2))
