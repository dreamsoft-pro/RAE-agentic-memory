from rae_task_bridge import RAETaskBridge
import json

def check_node1_models():
    bridge = RAETaskBridge()
    # Task type discovered in code: shell_command
    payload = {
        "command": "ollama list"
    }
    print("[*] Checking available models on Node1...")
    task = bridge.create_task("shell_command", payload)
    if "id" in task:
        result = bridge.wait_for_task(task["id"])
        print("\n--- OLLAMA MODELS ON NODE1 ---")
        if "stdout" in result:
            print(result["stdout"])
        else:
            print(result)
    else:
        print("Failed to create task.")

if __name__ == "__main__":
    check_node1_models()

