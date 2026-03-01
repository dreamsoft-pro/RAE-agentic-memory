from rae_task_bridge import RAETaskBridge
import json

def test_caps():
    bridge = RAETaskBridge()
    types = ["NODE1", "CODE_FACTORY", "DEEPSEEK", "OLLAMA", "LLM", "CODE_GENERATION"]
    payload = {"instruction": "test"}
    
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
    test_caps()
