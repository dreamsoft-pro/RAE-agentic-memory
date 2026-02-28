from rae_task_bridge import RAETaskBridge
import json

def test_shell():
    bridge = RAETaskBridge()
    payload = {"command": "hostname && nvidia-smi -L"}
    task = bridge.create_task("shell", payload)
    
    if "id" in task:
        print(f"Task created: {task['id']}")
        res = bridge.wait_for_task(task["id"])
        print(res)
    else:
        print(f"Creation failed: {task}")

if __name__ == "__main__":
    test_shell()
