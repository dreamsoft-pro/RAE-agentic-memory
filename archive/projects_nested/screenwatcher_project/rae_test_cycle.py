from rae_task_bridge import RAETaskBridge
import json

def test_code_verify_cycle():
    bridge = RAETaskBridge()
    
    # Próba wywołania cyklu jakości bezpośrednio na Node1
    # Payload dla pętli: prompt (zadanie), models (opcjonalnie)
    payload = {
        "prompt": "Write a robust Django Service class for processing OEE data. Ensure it handles DivisionByZero errors and uses transaction.atomic().",
        "model_generate": "deepseek-coder:33b",
        "model_audit": "deepseek-coder:6.7b"
    }
    
    print("[*] Creating task of type 'code_verify_cycle'...")
    task = bridge.create_task("code_verify_cycle", payload)
    
    if "id" in task:
        print(f"[*] Task created with ID: {task['id']}")
        result = bridge.wait_for_task(task["id"])
        print("\n--- CYCLE RESULT ---")
        print(json.dumps(result, indent=2))
    else:
        print(f"[-] Failed to create task: {task}")

if __name__ == "__main__":
    test_code_verify_cycle()
