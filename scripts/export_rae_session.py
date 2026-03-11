#!/usr/bin/env python3
import zipfile
import os
from pathlib import Path

# Lista plików i katalogów do spakowania (Skrypty + Kotwice + Core Logic)
FILES_TO_PACK = [
    "scripts/bootstrap_session.py",
    "scripts/sync_to_node1.sh",
    "scripts/sync_from_node1.sh",
    "scripts/wake_lumina.sh",
    "scripts/connect_cluster.py",
    "scripts/import_rae_session.py",
    "AUTO_RESUME.md",
    "DEVELOPER_CHEAT_SHEET.md",
    "GEMINI.md",
    ".rae_session",
    "pyproject.toml",
    "rae-core/rae_core/math/logic_gateway.py",
    "rae-core/rae_core/math/fusion.py",
    "rae-core/rae_core/math/resonance.py",
    "rae-core/rae_core/engine.py",
    "apps/memory_api/api/v2/memory.py",
    "apps/memory_api/services/rae_core_service.py"
]

OUTPUT_ZIP = "RAE_PORTABLE_STATE.zip"

def create_export():
    print(f"📦 Tworzę przenośny pakiet RAE: {OUTPUT_ZIP}...")
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in FILES_TO_PACK:
            if os.path.exists(file_path):
                print(f"  + Dodaję: {file_path}")
                zipf.write(file_path)
            else:
                print(f"  - Pomijam (nie znaleziono): {file_path}")

    print(f"\n✅ Gotowe! Przenieś {OUTPUT_ZIP} na pendrive.")

if __name__ == "__main__":
    create_export()