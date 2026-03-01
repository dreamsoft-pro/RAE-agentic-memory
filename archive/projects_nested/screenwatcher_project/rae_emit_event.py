import http.client
import json

def emit_test_event():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "tenant_id": "screenwatcher",
        "project_id": "screenwatcher_project",
        "event_type": "threshold_exceeded", # Use a supported enum value
        "payload": {
            "instruction": "Generate Advanced OEE Metrics",
            "target": "node1"
        }
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    try:
        conn.request("POST", "/v1/triggers/events/emit", json.dumps(payload), headers)
        res = conn.getresponse()
        print(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    emit_test_event()
