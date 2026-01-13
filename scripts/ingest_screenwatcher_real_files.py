import requests
import os

API_URL = "http://100.66.252.117:8000/v1/memory"
HEADERS = {
    "Content-Type": "application/json", 
    "X-Tenant-Id": "screenwatcher"
}
PROJECT = "screenwatcher_project"

# Paths relative to where the script is run (assuming run from cloud root or RAE folder)
# We will use absolute paths to be safe given we are in /home/grzegorz-lesniowski/cloud
BASE_DIR = "/home/grzegorz-lesniowski/cloud"

FILES_TO_INGEST = [
    {
        "path": os.path.join(BASE_DIR, "screenwatcher_project/DEVELOPMENT_PLAN.md"), 
        "layer": "semantic", 
        "tags": ["plan", "roadmap", "status", "architecture"]
    },
    {
        "path": os.path.join(BASE_DIR, "screenwatcher_project/GEMINI.md"), 
        "layer": "semantic", 
        "tags": ["rules", "protocol", "config", "agent-rules"]
    },
]

def ingest():
    print(f"🚀 Starting ingestion for project: {PROJECT}")
    for f in FILES_TO_INGEST:
        file_path = f["path"]
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping {file_path} (not found)")
            continue
            
        print(f"📖 Reading {file_path}...")
        with open(file_path, "r") as fd:
            content = fd.read()
            
        payload = {
            "content": content,
            "tags": f["tags"],
            "layer": f["layer"],
            "project": PROJECT,
            "metadata": {"source_file": file_path}
        }
        
        try:
            res = requests.post(f"{API_URL}/store", headers=HEADERS, json=payload)
            if res.status_code == 200:
                print(f"✅ Ingested {file_path}")
            else:
                print(f"❌ Failed to ingest {file_path}: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"⚠️ Error ingesting {file_path}: {e}")

if __name__ == "__main__":
    ingest()
