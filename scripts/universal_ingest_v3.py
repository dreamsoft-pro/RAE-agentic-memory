import httpx
import os
import re
from pathlib import Path

# Config
API_URL = 'http://localhost:8001/v2/memories/'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}
PROJECT_ROOT = Path(os.environ.get('RAE_PROJECT_ROOT', Path(__file__).resolve().parent.parent))
CLOUD_ROOT = PROJECT_ROOT.parent
FRONTEND_ROOT = str(PROJECT_ROOT / 'agent_hive' / 'work_dir' / 'components') if 'FRONTEND_ROOT' in ['OUT_DIR', 'WORK_DIR'] else str(CLOUD_ROOT / 'dreamsoft_factory' / 'frontend')
CHUNK_SIZE = 2500  # Characters

def chunk_text(text, size):
    """Simple chunking that tries to stay within bounds."""
    return [text[i:i+size] for i in range(0, len(text), size)]

def ingest_all():
    print(f"🚀 Starting Universal Code Ingest v3 (with Chunking) from {FRONTEND_ROOT}...")
    all_files = []
    
    if not os.path.exists(FRONTEND_ROOT):
        print(f"❌ ERROR: {FRONTEND_ROOT} not found on host!")
        return

    # Scan for both JS and HTML
    for root, dirs, files in os.walk(FRONTEND_ROOT):
        if 'node_modules' in root or '.git' in root: continue
        for file in files:
            if file.endswith((".js", ".html")):
                all_files.append(os.path.join(root, file))
    
    print(f"📦 Found {len(all_files)} source files.")
    
    total_chunks = 0
    for f_idx, f_path in enumerate(all_files):
        try:
            with open(f_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            s_name = os.path.basename(f_path)
            f_type = "template" if f_path.endswith(".html") else "logic"
            
            # Split into chunks
            chunks = chunk_text(content, CHUNK_SIZE)
            
            for c_idx, chunk_content in enumerate(chunks):
                payload = {
                    "content": chunk_content,
                    "layer": "semantic",
                    "tags": ["modernization_v3", "source_code", f_type],
                    "project": "DREAMSOFT PRO 2.0",
                    "metadata": {
                        "file": s_name,
                        "path": f_path.replace(FRONTEND_ROOT, ""),
                        "chunk_index": c_idx,
                        "total_chunks": len(chunks),
                        "type": f_type
                    }
                }
                
                # Use retries for stability
                for retry in range(3):
                    try:
                        r = httpx.post(API_URL, json=payload, headers=HEADERS, timeout=30.0)
                        if r.status_code == 200:
                            total_chunks += 1
                            break
                    except:
                        time.sleep(1)
            
            if (f_idx + 1) % 10 == 0:
                print(f"  -> Processed {f_idx + 1}/{len(all_files)} files (Total chunks: {total_chunks})...")
                
        except Exception as e:
            print(f"  ❌ Error processing {f_path}: {e}")
            
    print(f"✅ Finished. Ingested {total_chunks} chunks from {len(all_files)} files to RAE.")

if __name__ == '__main__':
    ingest_all()
