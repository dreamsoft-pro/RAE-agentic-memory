import os
import sys
from time import sleep

import requests

BASE_URL = "http://localhost:8001"
SESSION_FILE = ".rae_session"

def get_session_id():
    if not os.path.exists(SESSION_FILE):
        print("❌ Error: .rae_session file not found. Run bootstrap_session.py first.")
        sys.exit(1)
    with open(SESSION_FILE, "r") as f:
        return f.read().strip()

def verify_implicit_capture():
    session_id = get_session_id()
    print(f"🆔 Using Session ID: {session_id}")

    # 1. Execute an Action via RAE Agent Pipeline
    # This simulates an agent asking RAE to do something.
    # The Runtime should process this and IMPLICITLY save the result.
    print("\n🤖 Sending Prompt to Agent Pipeline...")

    prompt = f"Verify RAE-First implicit memory capture for session {session_id[:8]}. Just confirm this works."

    payload = {
        "tenant_id": "default-tenant",
        "project": "verification-agent",
        "prompt": prompt,
        "session_id": session_id
    }

    try:
        # Note: We use the /agent/execute endpoint which triggers the RAERuntime logic we modified
        resp = requests.post(f"{BASE_URL}/v1/agent/execute", json=payload, headers={"X-Tenant-Id": "default-tenant"})
        if resp.status_code != 200:
            print(f"❌ Agent Execution Failed: {resp.status_code} - {resp.text}")
            sys.exit(1)

        result = resp.json()
        print(f"✅ Agent Response: {result.get('answer')}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        sys.exit(1)

    print("\n⏳ Waiting 2s for async persistence...")
    sleep(2)

    # 2. Audit the Memory
    print("\n🔍 Auditing RAE Memory for Implicit Trace...")

    query_payload = {
        "query_text": session_id,  # Search for the session ID itself
        "project": "verification-agent",
        "k": 5
    }

    try:
        audit_resp = requests.post(f"{BASE_URL}/v1/memory/query", json=query_payload, headers={"X-Tenant-Id": "default-tenant"})
        memories = audit_resp.json().get("results", [])

        found = False
        for mem in memories:
            # Check metadata for session_id (it might be in metadata or just content if we searched text)
            # Ideally, we look at the 'metadata' field if exposed, or tags.
            # Our modified Query endpoint might not return full metadata in the top-level list,
            # but we can check content.

            # Note: The search logic matches content.
            # The implicitly stored memory should contain the answer or thought.

            print(f"   - Found Memory: {mem.get('content')[:100]}... (Score: {mem.get('score')})")

            # Deep check via Get Memory if possible, but let's rely on content match for now
            if session_id in str(mem):
                # This is unlikely to match unless session_id is in content.
                # However, our query was the session_id.
                pass

        # Since vector search is fuzzy, let's look for the SPECIFIC content we generated.
        # Or better, list memories by project and look for recent ones.

        list_resp = requests.get(
            f"{BASE_URL}/v1/memory/list?limit=5&project=verification-agent",
            headers={"X-Tenant-Id": "default-tenant"}
        )
        recent_memories = list_resp.json().get("results", [])

        print("\n📋 Recent Memories for 'verification-agent':")
        for mem in recent_memories:
            tags = mem.get("tags", [])
            print(f"   - [Tags: {tags}] {mem.get('content')[:50]}...")

            if "rae-first" in tags and "final_answer" in tags:
                found = True
                print("   🎉 SUCCESS! Found 'rae-first' and 'final_answer' tags. Implicit Capture Verified.")
                break

        if not found:
            print("\n❌ FAILURE: Could not find implicitly captured memory with 'rae-first' tag.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Audit Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_implicit_capture()
