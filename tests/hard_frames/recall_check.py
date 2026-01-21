import os
import sys
import requests
from rae_agent.security import apply_hard_frames

def query_rae(session, url, query_text, api_key, tenant_id):
    # Use exact keywords from the known content format:
    # "Machine=CNC-01 Sensor=pressure"
    payload = {
        "query_text": query_text,
        "k": 5,
        "project": "industrial_ultra_test"
        # We don't use 'filters' here because we learned that we didn't ingest structured metadata keys,
        # only tags. And RAE API might not map filters['machine_id'] to tags automatically.
        # So we rely on Content Matching (Hybrid Search logic inside RAE).
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Tenant-Id": tenant_id,
        "Content-Type": "application/json"
    }
    print(f"🔍 Querying: '{query_text}'...")
    try:
        resp = session.post(f"{url}/v1/memory/query", json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            print(f"✅ Found {len(results)} results.")
            for i, res in enumerate(results):
                content = res.get('content')
                score = res.get('score', 0.0)
                
                # Check alignment with query keywords
                # E.g. if query is "Machine=CNC-01", content must have it.
                keywords = [w for w in query_text.split() if "=" in w]
                matches = [k for k in keywords if k in content]
                
                is_perfect = len(matches) == len(keywords)
                
                status_icon = "🟢" if is_perfect else "🔴"
                print(f"   [{i+1}] {status_icon} (Score: {score:.4f}) {content[:120]}...")
        else:
            print(f"❌ Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def run_recall_check():
    print("🧠 STARTING PRECISION RECALL CHECK 🧠")
    
    base_url = os.getenv("RAE_KERNEL_URL", "http://rae-api-dev:8000")
    api_key = os.getenv("RAE_API_KEY", "dev-key")
    tenant_id = os.getenv("RAE_TENANT_ID", "00000000-0000-0000-0000-000000000000")
    
    apply_hard_frames()
    
    session = requests.Session()
    
    # Queries constructed to leverage the exact format of ingested data
    # format: "Machine=X Sensor=Y Status=Z"
    queries = [
        "Machine=PRESS-A Status=CRITICAL",
        "Sensor=vibration Machine=ROBOT-ARM-Z",
        "Machine=CNC-02 Sensor=temp Status=WARNING"
    ]
    
    for q in queries:
        query_rae(session, base_url, q, api_key, tenant_id)
        print("-" * 50)

if __name__ == "__main__":
    run_recall_check()
