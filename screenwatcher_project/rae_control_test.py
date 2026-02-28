from rae_task_bridge import RAETaskBridge
import json

def try_control_plane_delegation():
    bridge = RAETaskBridge()
    
    # Let's try to find the EXACT task type by listing node capabilities more deeply
    # or using a simple 'ping' task first.
    
    payload = {
        "instruction": "Generate Python class for OEE metrics MTBF and MTTR using Django ORM.",
        "context": "Django 5.2, models: DailyOEE, DowntimeEvent",
        "steps": [
            {"model": "deepseek", "action": "generate"},
            {"model": "ollama", "action": "audit"}
        ]
    }
    
    # Based on standard RAE Task format
    task = bridge.create_task("code_factory", payload)
    
    if "id" in task:
        print(f"Task created: {task['id']}")
        res = bridge.wait_for_task(task["id"])
        print(res)
    else:
        print(f"Creation failed: {task}")

if __name__ == "__main__":
    try_control_plane_delegation()
