# scripts/test_rae_fluidity.py
import os
import httpx
import asyncio
import json
import psycopg2
from datetime import datetime

# Configuration for Container Internal Network
API_URL = "http://localhost:8000/v2/bridge/interact"
DB_PARAMS = {
    "host": "rae-postgres", # Container name
    "user": "rae",
    "password": "rae_password",
    "dbname": "rae"
}
TENANT_ID = "53717286-fe94-4c8f-baf9-c4d2758eb672"
PROJECT_ID = "dreamsoft_factory"

async def fire_test_pulse():
    print(f"🚀 Firing Fluidity Pulse: {datetime.now().isoformat()}")
    
    payload = {
        "intent": "Perform a security and quality audit of the recent Header.tsx changes.",
        "context": {
            "project_id": PROJECT_ID,
            "tenant_id": TENANT_ID,
            "module_focus": ["rae-quality", "rae-phoenix"]
        },
        "metadata": {
            "source": "fluidity-test-v3.2",
            "info_class": "INTERNAL"
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(API_URL, json=payload, headers={"X-Tenant-Id": TENANT_ID, "X-Project-Id": PROJECT_ID})
            print(f"📡 Bridge Response Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print("✅ Oracle Decision received.")
                print(f"🤖 Pattern Detected: {data.get('pattern', 'UNKNOWN')}")
                return data.get('trace_id')
            else:
                print(f"❌ Bridge Failure: {resp.text}")
                return None
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return None

def verify_audit_trail(trace_id):
    if not trace_id:
        return
    
    print(f"🔍 Verifying Audit Trail in Database for Trace: {trace_id}")
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # Check for memories with this trace_id
        query = "SELECT content, metadata, reasoning, agent_id FROM memories WHERE (metadata->>'trace_id' = %s OR metadata->>'parent_trace_id' = %s);"
        cur.execute(query, (trace_id, trace_id))
        rows = cur.fetchall()
        
        if rows:
            print(f"✅ Found {len(rows)} audit records.")
            for row in rows:
                content_preview = row[0][:50] + "..."
                meta = row[1]
                reasoning = row[2]
                agent = row[3]
                
                print(f"--- Record ---")
                print(f"🤖 Agent: {agent}")
                print(f"📝 Content: {content_preview}")
                print(f"🧠 Reasoning: {reasoning}")
                print(f"🏢 Tenant: {meta.get('tenant_id')}")
                print(f"📁 Project: {meta.get('project_id')}")
                
                if meta.get('tenant_id') == TENANT_ID and meta.get('project_id') == PROJECT_ID:
                    print("✨ Metadata Integrity: VALID")
                else:
                    print("⚠️ Metadata Integrity: MISMATCH")
        else:
            print("❌ No audit trail found in database.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ DB Verification Error: {e}")

if __name__ == "__main__":
    trace_id = asyncio.run(fire_test_pulse())
    if trace_id:
        # Wait for worker to process
        print("⏳ Waiting for async processing...")
        import time
        time.sleep(5)
        verify_audit_trail(trace_id)
