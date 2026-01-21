import os
import sys
import requests
from rae_agent.security import apply_hard_frames

def query_rae(session, url, query_text, api_key, tenant_id):
    payload = {
        "query_text": query_text,
        "k": 20, # Increase recall window
        "project": "industrial_ultra_test"
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
            print(f"✅ Found {len(results)} results (Top 5 shown):")
            
            # Extract keywords for naive validation
            keywords = []
            if "PRESS-A" in query_text: keywords.append("PRESS-A")
            if "CRITICAL" in query_text: keywords.append("CRITICAL")
            if "ROBOT-ARM-Z" in query_text: keywords.append("ROBOT-ARM-Z")
            if "vibration" in query_text: keywords.append("vibration")
            
            hits = 0
            for i, res in enumerate(results[:5]): # Show top 5
                content = res.get('content')
                score = res.get('score', 0.0)
                
                # Check match
                is_hit = all(k in content for k in keywords)
                if is_hit: hits += 1
                
                status_icon = "🟢" if is_hit else "🔴"
                print(f"   [{i+1}] {status_icon} (Score: {score:.4f}) {content[:100]}...")
            
            if hits > 0:
                print(f"🎯 Precision@5: {hits}/5 relevant results.")
            else:
                print(f"⚠️  Precision@5: 0/5. Retrieval struggled.")
                
        else:
            print(f"❌ Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def run_recall_check():
    print("🧠 STARTING NATURAL LANGUAGE RECALL CHECK 🧠")
    
    base_url = os.getenv("RAE_KERNEL_URL", "http://rae-api-dev:8000")
    api_key = os.getenv("RAE_API_KEY", "dev-key")
    tenant_id = os.getenv("RAE_TENANT_ID", "00000000-0000-0000-0000-000000000000")
    
    apply_hard_frames()
    
    session = requests.Session()
    
    # Natural Language Queries tailored for Embedding Models
    queries = [
        "Find log entries where Machine is PRESS-A and Status is CRITICAL",
        "Retrieve vibration sensor readings for machine ROBOT-ARM-Z",
        "Search for warnings related to temperature on CNC-02"
    ]
    
    for q in queries:
        query_rae(session, base_url, q, api_key, tenant_id)
        print("-" * 50)

if __name__ == "__main__":
    run_recall_check()