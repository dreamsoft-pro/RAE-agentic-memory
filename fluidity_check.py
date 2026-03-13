import sys
import os
import time
import logging

# Ustawienie ścieżek dla rae_core
sys.path.append(os.path.abspath("./rae-core"))

from rae_core.utils.enterprise_guard import RAE_Enterprise_Foundation, audited_operation

class FluidityTester:
    def __init__(self):
        # Inicjalizacja z projektem 'performance_test'
        # RAEContextLocator powinien zmapować to na systemowy tenant 000...0
        self.enterprise_foundation = RAE_Enterprise_Foundation(module_name="performance_test")

    @audited_operation(operation_name="ping_pong_fluidity", impact_level="low")
    def run_test(self):
        print("🚀 Fluidity Test: Executing audited operation...")
        time.sleep(0.1) # Symulacja pracy
        return "Pong"

if __name__ == "__main__":
    # Wyciszenie logów dla czystego outputu testu
    logging.getLogger("RAE").setLevel(logging.WARNING)
    
    print("--- RAE SUITE FLUIDITY CHECK ---")
    start = time.time()
    
    tester = FluidityTester()
    init_time = time.time() - start
    print(f"✅ Foundation Init: {init_time:.4f}s")
    
    op_start = time.time()
    result = tester.run_test()
    time.sleep(1.0) # Wait for background threads to finish
    op_duration = time.time() - op_start
    
    print(f"✅ Operation Result: {result}")
    print(f"✅ Total Audit Cycle (2 events): {op_duration:.4f}s")
    
    # Sprawdzenie czy wspomnienia trafiły do bazy
    print("\n--- DATABASE VERIFICATION ---")
    os.system('docker exec rae-postgres psql -U rae -d rae -c "SELECT human_label, created_at FROM memories WHERE project=\'performance_test\' ORDER BY created_at DESC LIMIT 2;"')
    
    total = time.time() - start
    print(f"\n🏁 Total Test Duration: {total:.4f}s")
    if total < 1.0:
        print("🚀 STATUS: SUPER FLUID")
    else:
        print("⚠️ STATUS: LATENCY DETECTED")
