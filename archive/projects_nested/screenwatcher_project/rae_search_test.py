import http.client
import json

def search_known_content():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "query_text": "PyQt6 Operator Panel",
        "limit": 5
    }
    headers = {
        'X-Tenant-Id': 'screenwatcher',
        'Content-Type': 'application/json'
    }
    try:
        conn.request("POST", "/v1/memory/query", json.dumps(payload), headers)
        res = conn.getresponse()
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    search_known_content()
