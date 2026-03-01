import http.client
import json

def get_graph_stats():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    params = "?project_id=screenwatcher_project"
    headers = {'X-Tenant-Id': 'screenwatcher'}
    try:
        conn.request("GET", f"/v1/graph/stats{params}", headers=headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    print(json.dumps(get_graph_stats(), indent=2))
