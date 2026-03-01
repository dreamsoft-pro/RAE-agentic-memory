from rae_task_bridge import RAETaskBridge
import json

def test_execute_with_tools():
    bridge = RAETaskBridge()
    prompt = "Generate OEE MTBF logic. Use Node1 compute."
    body = {
        "tenant_id": "screenwatcher",
        "project": "screenwatcher_project",
        "prompt": prompt,
        "tools_allowed": ["node1"],
        "budget_tokens": 10000
    }
    # Using execute_agent logic but with tools
    conn = http.client.HTTPConnection("100.66.252.117", 8000)
    headers = {'X-Tenant-Id': 'screenwatcher', 'Content-Type': 'application/json'}
    conn.request("POST", "/v1/agent/execute", json.dumps(body), headers)
    print(conn.getresponse().read().decode("utf-8"))

if __name__ == "__main__":
    import http.client
    test_execute_with_tools()
