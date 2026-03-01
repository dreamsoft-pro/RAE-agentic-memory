from rae_task_bridge import RAETaskBridge
import json

def test_ollama():
    bridge = RAETaskBridge()
    payload = {
        "model": "deepseek-coder",
        "prompt": "Write a hello world in Python"
    }
    
    types = ["ollama", "deepseek", "llm_generation", "code_factory"]
    for t in types:
        print(f"\n[*] Trying task type: {t}")
        task = bridge.create_task(t, payload)
        if "id" in task:
            res = bridge.wait_for_task(task["id"])
            print(f"Result for {t}: {res}")
        else:
            print(f"Failed to create {t}")

if __name__ == "__main__":
    test_ollama()

