import sys
import os

# Ustawienie ścieżek
sys.path.append(os.path.abspath("./rae-core"))

from rae_core.utils.contract_manager import ContractManager

def bootstrap():
    cm = ContractManager()
    print(cm.get_bootstrap_summary())
    print("\n🚀 RAE SYSTEM: All agents are now bound by these Hard Contracts.")
    print("MANDATE: Do not violate these rules. Every action is audited.")

if __name__ == "__main__":
    bootstrap()
