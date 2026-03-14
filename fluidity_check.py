import sys
import os
import time
import logging
import asyncio

# Ustawienie ścieżek
sys.path.append(os.path.abspath("./rae-core"))

from rae_core.utils.enterprise_guard import RAE_Enterprise_Foundation, audited_operation

class FluidityTester:
    def __init__(self):
        self.enterprise_foundation = RAE_Enterprise_Foundation(module_name="dreamsoft_factory")

    @audited_operation(operation_name="tenant_resolution_check", impact_level="low")
    async def run_test(self):
        print("🚀 Fluidity Test: Checking tenant resolution for dreamsoft_factory...")
        return "OK"

async def main():
    os.environ["RAE_API_URL"] = "http://localhost:8001"
    os.environ["RAE_PROJECT_NAME"] = "dreamsoft_factory"
    
    tester = FluidityTester()
    await tester.run_test()
    
    print("\n⏳ Waiting for background logging...")
    await asyncio.sleep(3)
    
    print("\n--- DATABASE VERIFICATION ---")
    os.system("docker exec rae-postgres psql -U rae -d rae -c \"SELECT human_label, tenant_id, project FROM memories ORDER BY created_at DESC LIMIT 2;\"")

if __name__ == "__main__":
    asyncio.run(main())
