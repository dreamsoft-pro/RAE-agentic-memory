from rae_task_bridge import RAETaskBridge
import json

def test_host_types():
    bridge = RAETaskBridge()
    types = ["lumina", "kubus-gpu-01", "gpu", "cuda", "ollama_deepseek"]
    payload = {"instruction": "ping"}
    
    for t in types:
        print(f"[*] Testing: {t}")
        task = bridge.create_task(t, payload)
        if "id" in task:
            res = bridge.wait_for_task(task["id"], timeout=20)
            if res.get("output") != "unknown_task_type":
                print(f"[!!!] FOUND: {t}")
                return t
    return None

if __name__ == "__main__":
    test_host_types()
