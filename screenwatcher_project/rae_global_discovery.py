import http.client
import json

def global_discovery():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    # Search across all projects by setting project to None or empty
    queries = ["kubus-gpu-01", "lumina", "Ollama", "DeepSeek", "control plane", "task type", "node1"]
    
    results = {}
    for q in queries:
        payload = {
            "project": None,
            "query_text": q,
            "limit": 10
        }
        headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
        try:
            conn.request("POST", "/v1/memory/query", json.dumps(payload), headers)
            res = conn.getresponse()
            results[q] = json.loads(res.read().decode("utf-8"))
        except Exception as e:
            results[q] = {"error": str(e)}
    
    return results

if __name__ == "__main__":
    discovery = global_discovery()
    print(json.dumps(discovery, indent=2))
