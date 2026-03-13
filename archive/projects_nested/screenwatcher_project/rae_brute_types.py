from rae_task_bridge import RAETaskBridge
import json

def brute_force_types():
    bridge = RAETaskBridge()
    # These are high-probability task types for this kind of system
    types = [
        "node1", "node1_task", "compute", "code_factory", "factory", 
        "generate", "ollama", "deepseek", "task", "process", 
        "agent", "workflow", "node1_workflow", "kubus"
    ]
    
    payload = {
        "instruction": "Hello Node1, what is your name?",
        "model": "deepseek-coder"
    }
    
    for t in types:
        print(f"\n[*] TESTING TYPE: {t}")
        task = bridge.create_task(t, payload)
        if "id" in task:
            res = bridge.wait_for_task(task["id"], timeout=30)
            if res.get("output") != "unknown_task_type":
                print(f"[!!!] SUCCESS! Type '{t}' works!")
                print(f"Response: {res}")
                return t
            else:
                print(f"[-] Type '{t}' returned unknown_task_type.")
        else:
            print(f"[!] Failed to create task type '{t}'.")
    
    return None

if __name__ == "__main__":
    brute_force_types()

