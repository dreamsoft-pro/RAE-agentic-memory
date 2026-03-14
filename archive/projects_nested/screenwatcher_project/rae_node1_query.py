import http.client
import json

def query_specific_node():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "query_text": "kubus-gpu-01 lumina task delegation node1 factory",
        "limit": 10
    }
    headers = {
        'X-Tenant-Id': 'screenwatcher',
        'Content-Type': 'application/json'
    }
    try:
        conn.request("POST", "/v2/memories/query", json.dumps(payload), headers)
        res = conn.getresponse()
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    query_specific_node()