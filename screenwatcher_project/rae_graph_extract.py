import http.client
import json

def extract_graph():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project_id": "screenwatcher_project",
        "limit": 50,
        "auto_store": True
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v1/graph/extract", json.dumps(payload), headers)
        res = conn.getresponse()
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    extract_graph()
