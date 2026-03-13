import http.client
import json
import time
import sys

class RAETaskBridge:
    def __init__(self, tenant_id='screenwatcher', host='100.66.252.117', port=8000):
        self.tenant_id = tenant_id
        self.host = host
        self.port = port

    def _request(self, method, path, body=None):
        conn = http.client.HTTPConnection(self.host, self.port)
        headers = {
            'X-Tenant-Id': self.tenant_id,
            'Content-Type': 'application/json'
        }
        try:
            conn.request(method, path, json.dumps(body) if body else None, headers)
            res = conn.getresponse()
            return json.loads(res.read().decode("utf-8"))
        finally:
            conn.close()

    def create_task(self, task_type, payload, priority=0):
        body = {
            "type": task_type,
            "payload": payload,
            "priority": priority
        }
        print(f"[*] Creating task of type '{task_type}'...")
        return self._request("POST", "/control/tasks", body)

    def get_task_status(self, task_id):
        return self._request("GET", f"/control/tasks/{task_id}")

    def wait_for_task(self, task_id, timeout=300, poll_interval=5):
        start_time = time.time()
        print(f"[*] Waiting for task {task_id} to complete...")
        
        while time.time() - start_time < timeout:
            task = self.get_task_status(task_id)
            status = task.get("status")
            
            if status == "COMPLETED":
                print("\n[+] Task COMPLETED successfully.")
                return task.get("result")
            elif status == "FAILED":
                print("\n[-] Task FAILED.")
                return {"error": task.get("error")}
            
            print(".", end="", flush=True)
            time.sleep(poll_interval)
        
        return {"error": "Timeout reached"}

    def execute_agent(self, project, prompt, budget=20000):
        body = {
            "tenant_id": self.tenant_id,
            "project": project,
            "prompt": prompt,
            "budget_tokens": budget
        }
        print(f"[*] Executing Agentic Pipeline for project '{project}'...")
        return self._request("POST", "/v1/agent/execute", body)

    def log_lesson(self, project, content):
        payload = {
            "project": project,
            "layer": "reflective",
            "tag": "delegation_lesson",
            "content": content
        }
        self._request("POST", "/v1/memory/store", payload)

if __name__ == "__main__":
    # Test call if run directly
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        bridge = RAETaskBridge()
        t = bridge.create_task("ping", {"message": "Hello from Gemini CLI"})
        if "id" in t:
            result = bridge.wait_for_task(t["id"])
            print(f"Result: {result}")
