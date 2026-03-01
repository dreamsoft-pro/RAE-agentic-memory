import http.client
import json

def list_nodes():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    headers = {
        'X-Tenant-Id': 'screenwatcher'
    }
    try:
        conn.request("GET", "/control/nodes", headers=headers)
        res = conn.getresponse()
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_nodes()
