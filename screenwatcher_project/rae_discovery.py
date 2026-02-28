from rae_task_bridge import RAETaskBridge
import json

def get_node_capabilities():
    bridge = RAETaskBridge()
    # Try types that usually trigger discovery or are mandatory
    types = ["info", "status", "ping", "help"]
    
    for t in types:
        print(f"\n[*] Testing type: {t}")
        task = bridge.create_task(t, {"request": "list_supported_tasks"})
        if "id" in task:
            res = bridge.wait_for_task(task["id"], timeout=15)
            print(f"Result for {t}: {res}")

if __name__ == "__main__":
    get_node_capabilities()

