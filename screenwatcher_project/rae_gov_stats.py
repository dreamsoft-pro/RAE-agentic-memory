import http.client
import json

def get_gov_stats():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    headers = {'X-Tenant-Id': 'screenwatcher'}
    try:
        conn.request("GET", "/v1/governance/tenant/screenwatcher?days=30", headers=headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    print(json.dumps(get_gov_stats(), indent=2))
