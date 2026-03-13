import http.client
import json

def sync_master_plan():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "project": "screenwatcher_project",
        "layer": "reflective",
        "tag": "master_plan_v2",
        "content": "Updated Roadmap based on Agreement Annex 2. Key gaps identified: Edge Operator Panel, MTBF/MTTR metrics, SPC/Heatmap charts, and Block Rule Editor. Priority shifted to Phase 6: Edge Operator GUI and Data Transformation."
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    conn.request("POST", "/v1/memory/store", json.dumps(payload), headers)
    print(conn.getresponse().read().decode())

if __name__ == "__main__":
    sync_master_plan()
