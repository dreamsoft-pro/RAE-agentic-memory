import http.client
import json

def sync_completion():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "layer": "episodic",
        "tag": "phase_6_complete",
        "content": "Phase 6 implemented: Operator Panel GUI (PyQt6) added to edge_client/main.py. Data transformation pipeline (Regex, Map, Round) integrated into ROI processing. Configurator updated to support transformation rules."
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    conn.request("POST", "/v2/memories/store", json.dumps(payload), headers)
    print(conn.getresponse().read().decode())

if __name__ == "__main__":
    sync_completion()
