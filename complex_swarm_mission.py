import sys
import os
import time
import asyncio
from datetime import datetime

# Ustawienie ścieżek
sys.path.append(os.path.abspath("./RAE-agentic-memory/rae-core"))

from rae_core.utils.enterprise_guard import RAE_Enterprise_Foundation, audited_operation

class PhoenixModule:
    def __init__(self):
        self.enterprise_foundation = RAE_Enterprise_Foundation(module_name="rae-phoenix")
    
    @audited_operation(operation_name="initiate_ecosystem_audit", impact_level="medium")
    def start_mission(self):
        print("🔥 [PHOENIX] Starting Ecosystem Integrity Audit...")
        return {"status": "mission_started", "target": "Master Stack v5.0"}

class HiveModule:
    def __init__(self):
        self.enterprise_foundation = RAE_Enterprise_Foundation(module_name="rae-hive")
    
    @audited_operation(operation_name="analyze_swarm_topology", impact_level="low")
    def analyze_topology(self):
        print("🐝 [HIVE] Analyzing Swarm Topology and Port Mappings...")
        time.sleep(0.2)
        return {"conflicts": 0, "active_nodes": 5}

class QualityModule:
    def __init__(self):
        self.enterprise_foundation = RAE_Enterprise_Foundation(module_name="rae-quality")
    
    @audited_operation(operation_name="security_frame_scan", impact_level="high")
    def run_security_scan(self):
        print("🛡️ [QUALITY] Running Hard Frames Security Scan...")
        time.sleep(0.3)
        return {"leaks": "none", "policy": "ISO 27001 compliant"}

class LabModule:
    def __init__(self):
        self.enterprise_foundation = RAE_Enterprise_Foundation(module_name="rae-lab")
    
    @audited_operation(operation_name="aggregate_mission_telemetry", impact_level="low")
    def finalize_telemetry(self, start_time):
        duration = time.time() - start_time
        print(f"📊 [LAB] Mission completed in {duration:.2f}s. Aggregating metrics...")
        return {"total_duration": duration, "efficiency": "optimal"}

async def run_complex_task():
    print("--- STARTING 3-PART COMPLEX RAE MISSION ---")
    mission_start = time.time()
    
    # 1. Phoenix Starts
    phoenix = PhoenixModule()
    phoenix.start_mission()
    
    # 2. Hive Analyzes
    hive = HiveModule()
    hive.analyze_topology()
    
    # 3. Quality Scans
    quality = QualityModule()
    quality.run_security_scan()
    
    # 4. Lab Finalizes
    lab = LabModule()
    lab.finalize_telemetry(mission_start)
    
    # Wait for async background logging to finish
    print("\n⏳ Waiting for asynchronous Memory Bridge to flush events...")
    await asyncio.sleep(2.0)
    print("🏁 Mission Finished.")

if __name__ == "__main__":
    # Ustawienie API URL na lokalny port API
    os.environ["RAE_API_URL"] = "http://localhost:8001"
    os.environ["RAE_PROJECT_NAME"] = "dreamsoft_factory"
    
    asyncio.run(run_complex_task())
