import sys
import os
import subprocess

# Path setup
sys.path.append(os.path.abspath("./rae-core"))
from rae_core.utils.contract_manager import ContractManager

def verify_volumes():
    print("🛡️ Verifying Data Locator Contract...")
    try:
        with open("/mnt/extra_storage/RAE-agentic-memory/docker-compose.yml", 'r') as f:
            content = f.read()
            if "rae-node-agent_postgres_data" not in content:
                print("❌ VIOLATION: POSTGRES_DATA volume is NOT pointing to rae-node-agent_postgres_data!")
                return False
        print("✅ Volumes match Data Locator Contract.")
        return True
    except Exception as e:
        print(f"⚠️ Could not verify volumes: {e}")
        return False

def bootstrap():
    cm = ContractManager()
    print(cm.get_bootstrap_summary())
    verify_volumes()
    print("\n🚀 RAE SYSTEM: All agents are now bound by these Hard Contracts.")

if __name__ == "__main__":
    bootstrap()
