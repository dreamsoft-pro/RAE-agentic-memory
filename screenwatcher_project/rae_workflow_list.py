import http.client
import json

def list_workflows():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    headers = {
        'X-Tenant-Id': 'screenwatcher'
    }
    try:
        # According to OpenAPI: GET /v1/triggers/workflows
        params = "?tenant_id=screenwatcher&project_id=screenwatcher_project"
        conn.request("GET", f"/v1/triggers/workflows{params}", headers=headers)
        res = conn.getresponse()
        print("--- Workflows ---")
        print(res.read().decode("utf-8"))
        
        # Also try templates
        conn.request("GET", "/v1/triggers/templates", headers=headers)
        res = conn.getresponse()
        print("\n--- Templates ---")
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_workflows()

