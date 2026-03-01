import http.client
import json

def search_workflow_node1():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "query_text": "Workflow Node1 DeepSeek Ollama Audyt Linter",
        "limit": 10
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v1/memory/query", json.dumps(payload), headers)
        res = conn.getresponse()
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    search_workflow_node1()
