from rae_task_bridge import RAETaskBridge
import json

def test_node1_factory():
    bridge = RAETaskBridge()
    payload = {
        "instruction": "test",
        "steps": ["generate", "audit"]
    }
    task = bridge.create_task("node1_factory", payload)
    if "id" in task:
        print(bridge.wait_for_task(task["id"]))

if __name__ == "__main__":
    test_node1_factory()
