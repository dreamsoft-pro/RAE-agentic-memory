import http.client
import json

def find_completed_tasks():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    # Search for completion logs
    payload = {
        "project": None,
        "query_text": "Task COMPLETED successfully result",
        "limit": 50
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
    result = find_completed_tasks()
    print(json.dumps(result, indent=2))
