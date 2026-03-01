from rae_task_bridge import RAETaskBridge
import json

def test_default():
    bridge = RAETaskBridge()
    task = bridge.create_task("default", {"instruction": "ping"})
    if "id" in task:
        print(bridge.wait_for_task(task["id"]))

if __name__ == "__main__":
    test_default()
