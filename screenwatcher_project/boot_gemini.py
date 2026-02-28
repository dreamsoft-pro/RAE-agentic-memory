import http.client
import json
import os
import subprocess

def rae_request(method, path, body):
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    headers = {
        'X-Tenant-Id': 'screenwatcher',
        'Content-Type': 'application/json'
    }
    try:
        conn.request(method, path, json.dumps(body), headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        if not data:
            return {}
        return json.loads(data)
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def get_git_status():
    try:
        res = subprocess.run(["git", "status"], capture_output=True, text=True)
        return res.stdout
    except:
        return "Unknown"

# 1. Store session start
rae_request("POST", "/v1/memory/store", {
    "project": "screenwatcher_project",
    "layer": "episodic",
    "tag": "session_start",
    "content": f"Session started. Git status: {get_git_status()[:200]}..."
})

# 2. Query recent context
print("Recent context from RAE:")
context = rae_request("POST", "/v1/memory/query", {
    "project": "screenwatcher_project",
    "query_text": "status task plan",
    "limit": 5
})
print(json.dumps(context, indent=2))
