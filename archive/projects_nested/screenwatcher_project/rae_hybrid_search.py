import http.client
import json

def hybrid_search():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "tenant_id": "screenwatcher",
        "project_id": "screenwatcher_project",
        "query": "How to use Node1 Code Factory task type protocol",
        "k": 20
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v1/search/hybrid", json.dumps(payload), headers)
        res = conn.getresponse()
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    hybrid_search()
