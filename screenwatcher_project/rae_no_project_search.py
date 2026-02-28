import http.client
import json

def search_no_project():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "query_text": "the",
        "k": 100
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v1/memory/query", json.dumps(payload), headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    res = search_no_project()
    if "results" in res:
        for r in res["results"]:
            print(f"[{r.get('project')}] {r.get('content')[:100]}...")
    else:
        print(res)
