from rae_task_bridge import RAETaskBridge
import json

def brute_force_camel():
    bridge = RAETaskBridge()
    types = [
        "CodeFactory", "Node1", "LLM", "Shell", "Task", "Factory", 
        "CodeGeneration", "Audit", "Linter", "DeepSeek", "Ollama"
    ]
    
    payload = {"instruction": "test"}
    for t in types:
        print(f"\n[*] TESTING: {t}")
        task = bridge.create_task(t, payload)
        if "id" in task:
            res = bridge.wait_for_task(task["id"], timeout=30)
            if res.get("output") != "unknown_task_type":
                print(f"[!!!] SUCCESS: {t}")
                return t
    return None

if __name__ == "__main__":
    brute_force_camel()

