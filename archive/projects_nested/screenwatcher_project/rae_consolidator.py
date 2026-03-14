import http.client
import json

def query_rae(project_name):
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": project_name,
        "query_text": "",  # Trying empty string
        "limit": 50
    }
    headers = {
        'X-Tenant-Id': 'screenwatcher',
        'Content-Type': 'application/json'
    }
    try:
        conn.request("POST", "/v2/memories/query", json.dumps(payload), headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    projects = ["screenwatcher", "screen_watcher", "screenwatcher_project"]
    all_memories = []
    
    for p in projects:
        print(f"Querying project: {p}")
        result = query_rae(p)
        if isinstance(result, list):
            for mem in result:
                mem['original_project'] = p
                all_memories.append(mem)
        elif isinstance(result, dict) and "results" in result:
             for mem in result["results"]:
                mem['original_project'] = p
                all_memories.append(mem)

    # Consolidate
    if all_memories:
        print(f"Found {len(all_memories)} total memories. Consolidating...")
        
        # Merge content
        combined_content = "CONSOLIDATED KNOWLEDGE BASE FROM FRAGMENTED PROJECTS:\n\n"
        for m in all_memories:
            combined_content += f"--- Source: {m['original_project']} ({m.get('tag', 'no-tag')}) ---\n"
            combined_content += f"{m['content']}\n\n"
            
        # Store back to primary
        conn = http.client.HTTPConnection("100.66.252.117", 8000)
        store_payload = {
            "project": "screenwatcher_project",
            "layer": "semantic",
            "tag": "consolidated_kb",
            "content": combined_content
        }
        headers = {
            'X-Tenant-Id': 'screenwatcher',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v2/memories/store", json.dumps(store_payload), headers)
        res = conn.getresponse()
        print(f"Consolidation result: {res.read().decode('utf-8')}")
    else:
        print("No fragmented memories found to consolidate.")