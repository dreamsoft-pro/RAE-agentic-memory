import http.client
import json

def get_triggers_info():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    headers = {'X-Tenant-Id': 'screenwatcher'}
    try:
        conn.request("GET", "/v1/triggers/info", headers=headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    info = get_triggers_info()
    print(json.dumps(info, indent=2))
