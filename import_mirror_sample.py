import json
import requests
import os
from pathlib import Path

API_URL = "http://localhost:8001/v2/memories/"
TENANT_ID = "53717286-fe94-4c8f-baf9-c4d2758eb672" # Dreamsoft
SOURCE_FILE = os.environ.get('RAE_SOURCE_FILE', str(Path(__file__).resolve().parent.parent / 'SOURCE_FILE_default'))

def test_import():
    print("🚀 Starting Mirror Sample Import Test...")
    
    with open(SOURCE_FILE, 'r') as f:
        # Pobieramy tylko pierwsze 3 chunki jako próbkę
        for line in f:
            line = f.readline()
            if not line: break
            
            data = json.loads(line)
            content = data.get("text", "")
            symbol_name = data.get("name", "unknown")
            kind = data.get("kind", "unknown")
            
            payload = {
                "content": content,
                "project": "dreamsoft_factory",
                "human_label": f"[MIRROR] {kind.upper()}: {symbol_name}",
                "layer": "semantic",
                "metadata": {
                    "source": "operacja_lustro_ingestia",
                    "original_path": data.get("filePath"),
                    "kind": kind,
                    "dependencies": data.get("dependenciesDI", [])
                }
            }
            
            headers = {"X-Tenant-Id": TENANT_ID}
            r = requests.post(API_URL, json=payload, headers=headers)
            
            if r.status_code in [200, 201]:
                print(f"✅ Imported {symbol_name} (ID: {r.json().get('memory_id')})")
            else:
                print(f"❌ Failed to import {symbol_name}: {r.text}")

if __name__ == "__main__":
    test_import()
