import os
import sys
import requests
from rae_agent.security import apply_hard_frames

def query_rae(session, url, query_text, filters, api_key, tenant_id):
    payload = {
        "query_text": query_text,
        "k": 5,
        "project": "industrial_ultra_v3", # Query the NEW fresh project
        "filters": filters
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Tenant-Id": tenant_id,
        "Content-Type": "application/json"
    }
    print(f"🔍 Querying: '{query_text}' | Filters: {filters}...")
    try:
        resp = session.post(f"{url}/v1/memory/query", json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            print(f"✅ Found {len(results)} results.")
            for i, res in enumerate(results):
                content = res.get('content')
                score = res.get('score', 0.0)
                meta = res.get('metadata', {})
                
                # Check if filters were respected by checking the returned metadata
                # (Note: RAE returns metadata in results)
                matches_filter = True
                for f_key, f_val in filters.items():
                    if meta.get(f_key) != f_val:
                        matches_filter = False
                        break
                
                status_icon = "🟢" if matches_filter else "🔴"
                print(f"   [{i+1}] {status_icon} (Score: {score:.4f}) {content[:100]}...")
        else:
            print(f"❌ Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def run_recall_check():
    print("🧠 STARTING ULTIMATE PRECISION RECALL CHECK (Metadata Filtering) 🧠")
    
    base_url = os.getenv("RAE_KERNEL_URL", "http://rae-api-dev:8000")
    api_key = os.getenv("RAE_API_KEY", "dev-key")
    tenant_id = os.getenv("RAE_TENANT_ID", "00000000-0000-0000-0000-000000000000")
    
    apply_hard_frames()
    
    session = requests.Session()
    
    # We now use the ACTUAL metadata keys we ingested in v3
    scenarios = [
        {
            "q": "Critical events from Press-A",
            "f": {"machine_id": "PRESS-A", "machine_status": "CRITICAL"}
        },
        {
            "q": "Vibration on Robot Arm Z",
            "f": {"machine_id": "ROBOT-ARM-Z", "sensor_type": "vibration"}
        },
        {
            "q": "CNC-02 normal operation",
            "f": {"machine_id": "CNC-02", "machine_status": "NORMAL"}
        }
    ]
    
    for s in scenarios:
        query_rae(session, base_url, s["q"], s["f"], api_key, tenant_id)
        print("-" * 50)

if __name__ == "__main__":
    run_recall_check()
