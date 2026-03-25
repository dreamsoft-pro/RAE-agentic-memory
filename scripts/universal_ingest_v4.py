import httpx
import os
import re
from pathlib import Path
import time

# v4.1 - Perfect Ingest (Stable Encoding)
API_URL = 'http://localhost:8001/v2/memories/'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}
PROJECT_ROOT = Path(os.environ.get('RAE_PROJECT_ROOT', Path(__file__).resolve().parent.parent))
CLOUD_ROOT = PROJECT_ROOT.parent
FRONTEND_ROOT = str(PROJECT_ROOT / 'agent_hive' / 'work_dir' / 'components') if 'FRONTEND_ROOT' in ['OUT_DIR', 'WORK_DIR'] else str(CLOUD_ROOT / 'dreamsoft_factory' / 'frontend')
CHUNK_SIZE = 3000

BANNED_FILES = ['jquery', 'lodash', 'bootstrap', 'cropper', 'moment', 'angular.', 'tinymce', 'caman', 'select2']

def chunk_text(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def ingest_all():
    print("🚀 Starting Perfect Ingest v4.1...")
    all_files = []
    
    if not os.path.exists(FRONTEND_ROOT):
        print("❌ ERROR: Path not found!")
        return

    for root, dirs, files in os.walk(FRONTEND_ROOT):
        if any(b in root.lower() for b in ['node_modules', '.git', 'dist']): continue
        for file in files:
            if file.endswith((".js", ".html")):
                if not any(b in file.lower() for b in BANNED_FILES):
                    all_files.append(os.path.join(root, file))
    
    print("📦 Found " + str(len(all_files)) + " custom source files.")
    
    total_chunks = 0
    for f_idx, f_path in enumerate(all_files):
        try:
            with open(f_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            s_name = os.path.basename(f_path)
            f_type = "template" if f_path.endswith(".html") else "logic"
            chunks = chunk_text(content, CHUNK_SIZE)
            
            for c_idx, chunk_content in enumerate(chunks):
                # Avoid f-string newlines for stable scp
                header = "FILE: " + s_name + " (chunk " + str(c_idx) + "/" + str(len(chunks)) + ")"
                augmented_content = header + chr(10) + chr(10) + chunk_content
                
                payload = {
                    "content": augmented_content,
                    "layer": "semantic",
                    "tags": ["modernization_v3", "source_code", f_type],
                    "project": "DREAMSOFT PRO 2.0",
                    "metadata": {
                        "file": s_name,
                        "chunk_index": c_idx,
                        "total_chunks": len(chunks),
                        "type": f_type
                    }
                }
                
                for retry in range(3):
                    try:
                        r = httpx.post(API_URL, json=payload, headers=HEADERS, timeout=30.0)
                        if r.status_code == 200:
                            total_chunks += 1
                            break
                    except:
                        time.sleep(1)
            
            if (f_idx + 1) % 10 == 0:
                print("  -> Processed " + str(f_idx + 1) + "/" + str(len(all_files)) + " files...")
                
        except Exception as e:
            print("  ❌ Error: " + str(e))
            
    print("✅ Finished. Ingested " + str(total_chunks) + " chunks.")

if __name__ == '__main__':
    ingest_all()
