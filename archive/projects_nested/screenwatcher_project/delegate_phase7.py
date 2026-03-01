from rae_task_bridge import RAETaskBridge
import json

def delegate_phase_7():
    bridge = RAETaskBridge()
    
    prompt = """
    PROJECT: screenwatcher_project
    TASK: Generate Advanced OEE Metrics Service
    CONTEXT:
    - Django 5.2, Python 3.13
    - Existing Models in 'apps.oee.models': DailyOEE, ShiftOEE, DowntimeEvent
    - Goal: Implement OEEMetricsService in 'apps/oee/services.py'
    
    REQUIRED METHODS:
    1. calculate_mtbf(machine, start_date, end_date): 
       Formula: (Total Operating Time) / (Number of Failures). 
       A 'Failure' is a DowntimeEvent where reason is not 'SETUP' or 'PLANNED'.
    2. calculate_mttr(machine, start_date, end_date):
       Formula: (Total Maintenance Time) / (Number of Repairs).
    3. calculate_scrap_rate(machine, start_date, end_date):
       Aggregation of (parts - good_parts) / total_parts from DailyOEE.
    4. calculate_operator_efficiency(machine, operator_id, date):
       Actual production / (Shift duration * Target Rate).
    
    OUTPUT FORMAT:
    Return ONLY the Python code for the OEEMetricsService class. 
    Handle division by zero. Use timezone-aware queries.
    """
    
    payload = {
        "instruction": prompt,
        "model": "deepseek-coder", # Typical model for Node1
        "system_prompt": "You are Node1, the Code Factory. You generate high-quality Python code for the ScreenWatcher project."
    }
    
    print("[*] Dispatching task to RAE Agentic Pipeline...")
    result = bridge.execute_agent("screenwatcher_project", prompt)
    
    if "answer" in result:
        print("\n--- RAE RESPONSE ---")
        print(result["answer"])
        
        # Log to RAE
        bridge.log_lesson("screenwatcher_project", "Successfully generated KPI logic using RAE Execute Pipeline. Node1 likely handled the backend compute.")
    else:
        print(f"Failed to execute: {result}")

if __name__ == "__main__":
    delegate_phase_7()
