import http.client
import json

def test_graph():
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    payload = {
        "tenant_id": "screenwatcher",
        "project_id": "screenwatcher_project",
        "node_id": "test_node_1",
        "label": "Test Node",
        "properties": {"info": "node1 discovery"}
    }
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    conn.request("POST", "/v1/graph-management/nodes", json.dumps(payload), headers)
    print(f"Store result: {conn.getresponse().read().decode()}")
    
    conn.request("GET", "/v1/graph/nodes?project_id=screenwatcher_project", headers=headers)
    print(f"List result: {conn.getresponse().read().decode()}")

if __name__ == "__main__":
    test_graph()
