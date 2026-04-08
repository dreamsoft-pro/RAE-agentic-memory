import json
import requests
import os
from pathlib import Path

API_URL = "http://localhost:8001/v2/memories/"
TENANT_ID = "53717286-fe94-4c8f-baf9-c4d2758eb672"
SOURCE_FILE = os.environ.get('RAE_SOURCE_FILE', str(Path(__file__).resolve().parent.parent / 'SOURCE_FILE_default'))

def run_import():
    print("🚀 Starting Mirror Import with Advanced Tagging...")
    
    with open(SOURCE_FILE, 'r') as f:
        for line in f:
            if not line.strip(): continue
            data = json.loads(line)
            
            content = data.get("text", "")
            symbol_name = data.get("name", "unknown")
            kind = data.get("kind", "unknown")
            
            # Budowanie tagów
            tags = ["dreamsoft", "angularjs", "nextjs", f"kind:{kind}"]
            if "Service" in symbol_name: tags.append("service")
            if "Ctrl" in symbol_name: tags.append("controller")
            
            payload = {
                "content": content,
                "project": "dreamsoft_factory",
                "human_label": f"[MIRROR][{kind.upper()}] {symbol_name}",
                "layer": "semantic",
                "tags": tags,
                "metadata": {
                    "source": "operacja_lustro_v2",
                    "original_path": data.get("filePath"),
                    "kind": kind,
                    "dependencies": data.get("dependenciesDI", []),
                    "migration_status": "pending_refactor"
                }
            }
            
            headers = {"X-Tenant-Id": TENANT_ID}
            try:
                r = requests.post(API_URL, json=payload, headers=headers, timeout=5)
                if r.status_code in [200, 201]:
                    print(f"✅ {symbol_name} tagged and saved.")
                else:
                    print(f"⚠️ Error saving {symbol_name}: {r.text[:100]}")
            except Exception as e:
                print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    run_import()
