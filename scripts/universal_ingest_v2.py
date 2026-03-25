import httpx
import os
from pathlib import Path

# Connect to RAE API on port 8001 (host access)
API_URL = 'http://localhost:8001/v2/memories/'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}
# Physical path on Node 1 host
PROJECT_ROOT = Path(os.environ.get('RAE_PROJECT_ROOT', Path(__file__).resolve().parent.parent))
CLOUD_ROOT = PROJECT_ROOT.parent
FRONTEND_ROOT = str(PROJECT_ROOT / 'agent_hive' / 'work_dir' / 'components') if 'FRONTEND_ROOT' in ['OUT_DIR', 'WORK_DIR'] else str(CLOUD_ROOT / 'dreamsoft_factory' / 'frontend')

def ingest_html():
    print(f"🚀 Starting Universal HTML Ingest for Phase 2 from {FRONTEND_ROOT}...")
    html_files = []
    
    if not os.path.exists(FRONTEND_ROOT):
        print(f"❌ ERROR: {FRONTEND_ROOT} not found on host!")
        return

    for root, dirs, files in os.walk(FRONTEND_ROOT):
        for file in files:
            if file.endswith(".html") and 'node_modules' not in root:
                html_files.append(os.path.join(root, file))
    
    print(f"📦 Found {len(html_files)} templates.")
    
    count = 0
    for f_path in html_files:
        try:
            with open(f_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            s_name = os.path.basename(f_path)
            payload = {
                "content": content,
                "layer": "semantic",
                "tags": ["html_template", "dreamsoft_v2", "phase2_pending"],
                "metadata": {
                    "file": s_name,
                    "path": f_path.replace(FRONTEND_ROOT, ""),
                    "type": "template"
                }
            }
            # Sending directly to host API
            httpx.post(API_URL, json=payload, headers=HEADERS, timeout=30.0)
            count += 1
            if count % 10 == 0:
                print(f"  -> Ingested {count}/{len(html_files)}...")
        except Exception as e:
            print(f"  ❌ Error ingesting {f_path}: {e}")
            
    print(f"✅ Finished. Ingested {count} templates to RAE.")

if __name__ == '__main__':
    ingest_html()
