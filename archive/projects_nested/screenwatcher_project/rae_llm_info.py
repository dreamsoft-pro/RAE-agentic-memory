import http.client
import json

def search_llm_info():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "query_text": "Ollama DeepSeek configuration node",
        "limit": 10
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    conn.request("POST", "/v2/memories/query", json.dumps(payload), headers)
    print(conn.getresponse().read().decode())

if __name__ == "__main__":
    search_llm_info()
