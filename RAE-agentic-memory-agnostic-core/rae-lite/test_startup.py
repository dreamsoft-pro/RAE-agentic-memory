
import sys
import os
from pathlib import Path

# Add project root to sys.path to allow imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "rae-core"))

print("Testing RAE-Lite startup...")

try:
    from rae_lite.server import app
    print("✅ RAE-Lite server initialized successfully.")
except Exception as e:
    print(f"❌ Startup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
