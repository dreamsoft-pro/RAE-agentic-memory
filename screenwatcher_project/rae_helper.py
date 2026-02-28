import requests
import json
import sys

BASE_URL = "http://localhost:8001"
HEADERS = {
    "X-Tenant-Id": "screenwatcher",
    "Content-Type": "application/json"
}

def store_memory(layer, tag, content):
    data = {
        "layer": layer,
        "tag": tag,
        "content": content,
        "project": "screenwatcher_project"
    }
    response = requests.post(f"{BASE_URL}/v1/memory/store", headers=HEADERS, json=data)
    return response.json()

def query_memory(query_text, limit=10):
    data = {
        "query_text": query_text,
        "project": "screenwatcher_project",
        "limit": limit
    }
    response = requests.post(f"{BASE_URL}/v1/memory/query", headers=HEADERS, json=data)
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rae_helper.py [store|query] ...")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "store":
        print(json.dumps(store_memory(sys.argv[2], sys.argv[3], sys.argv[4])))
    elif cmd == "query":
        print(json.dumps(query_memory(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 10)))
