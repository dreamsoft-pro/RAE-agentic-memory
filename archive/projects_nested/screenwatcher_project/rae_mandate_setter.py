import http.client
import json

def set_unified_mandate():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    # Define a rule in Semantic Layer to map all similar project names to the main one
    payload = {
        "project": "screenwatcher_project",
        "layer": "semantic",
        "tag": "project_mapping",
        "content": "RULE: All memories related to 'screenwatcher', 'screen_watcher', or 'screenwatcher_project' belong to the same project. The canonical project name is 'screenwatcher_project'. All future stores and queries must use this project name."
    }
    headers = {
        'X-Tenant-Id': 'screenwatcher',
        'Content-Type': 'application/json'
    }
    try:
        conn.request("POST", "/v2/memories/store", json.dumps(payload), headers)
        res = conn.getresponse()
        print(f"Unified mandate stored: {res.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    set_unified_mandate()
