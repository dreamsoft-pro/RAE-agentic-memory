from rae_task_bridge import RAETaskBridge
import json

def test_node1_inference():
    bridge = RAETaskBridge()
    # Task type: llm_inference
    # Payload requires model and prompt
    payload = {
        "model": "deepseek-coder:6.7b",
        "prompt": "Write a python function to add two numbers."
    }
    task = bridge.create_task("llm_inference", payload)
    if "id" in task:
        print(f"[*] Task created with ID: {task['id']}")
        result = bridge.wait_for_task(task["id"])
        print("\n--- INFERENCE RESULT ---")
        print(result)

if __name__ == "__main__":
    test_node1_inference()
