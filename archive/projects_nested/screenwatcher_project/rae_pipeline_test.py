from rae_task_bridge import RAETaskBridge
import json

def test_pipeline():
    bridge = RAETaskBridge()
    # If the worker script on Node1 is using a custom workflow, 
    # it might expect a 'workflow' task type.
    
    payload = {
        "steps": [
            {"action": "generate", "model": "deepseek"},
            {"action": "audit", "model": "ollama"}
        ],
        "input": "Write a Python script to calculate OEE."
    }
    
    # Testing 'workflow' which is a standard pattern in RAE
    print("[*] Testing 'workflow' task type...")
    task = bridge.create_task("workflow", payload)
    if "id" in task:
        print(bridge.wait_for_task(task["id"]))

if __name__ == "__main__":
    test_pipeline()
