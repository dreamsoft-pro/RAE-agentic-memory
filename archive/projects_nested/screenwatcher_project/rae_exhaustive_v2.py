from rae_task_bridge import RAETaskBridge
import json

def exhaustive_v2():
    bridge = RAETaskBridge()
    node_uuid = "b31d15e4-f328-4b5c-819a-d8d73e050539"
    
    types = ["code_factory", "factory", "agent", "worker", "gpu_task"]
    
    for t in types:
        print(f"\n[*] Trying task type: {t}")
        payload = {
            "assigned_node_id": node_uuid,
            "instruction": "test",
            "model": "deepseek-coder"
        }
        task = bridge.create_task(t, payload)
        if "id" in task:
            res = bridge.wait_for_task(task["id"])
            print(f"Result for {t}: {res}")

if __name__ == "__main__":
    exhaustive_v2()

