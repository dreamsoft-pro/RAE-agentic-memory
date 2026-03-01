from rae_task_bridge import RAETaskBridge
import json

def delegate_advanced_kpi():
    bridge = RAETaskBridge()
    
    # Precyzyjna specyfikacja dla Node1
    prompt = """
    TASK: Implement Advanced OEE & Reliability Metrics Service
    PROJECT: screenwatcher_project
    CONTEXT:
    - Django 5.2, Python 3.13
    - Models: apps.oee.models (DailyOEE, ShiftOEE, DowntimeEvent)
    - Source: apps.telemetry.models (TelemetryPoint)
    
    LOGIC TO IMPLEMENT in 'apps/oee/services.py':
    1. MTBF (Mean Time Between Failures): 
       - Sum of (Operating Time) / Count of (Failure Events).
       - Failure Event: DowntimeEvent where reason is NOT 'planned' or 'maintenance'.
    2. MTTR (Mean Time To Repair):
       - Sum of (Repair Time) / Count of (Repair Events).
    3. Scrap Rate %:
       - (Total Parts - Good Parts) / Total Parts * 100.
    4. Operator Performance Index:
       - Actual Output / (Standard Rate * Run Time).
    
    WORKFLOW:
    - DeepSeek: Write robust, timezone-aware Django ORM queries.
    - Ollama: Perform security audit and check for 'DivisionByZero' errors.
    
    OUTPUT: Return only the final OEEMetricsService class code.
    """
    
    # We use the 'code_factory' task type as per GEMINI.md
    payload = {
        "instruction": prompt,
        "workflow": "deepseek_generation_ollama_audit",
        "target_node": "kubus-gpu-01"
    }
    
    # Using the generic execute_agent to trigger the complex pipeline in RAE
    print("[*] Dispatching to RAE Agentic Pipeline (Node1 Factory)...")
    result = bridge.execute_agent("screenwatcher_project", prompt)
    
    if "answer" in result:
        print("\n--- CODE FACTORY RESULT ---")
        print(result["answer"])
        with open("phase7_code.txt", "w", encoding="utf-8") as f:
            # We save to temp file to read it carefully
            f.write(result["answer"])
    else:
        print(f"[-] Delegation failed: {result}")

if __name__ == "__main__":
    delegate_advanced_kpi()
