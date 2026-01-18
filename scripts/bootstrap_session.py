#!/usr/bin/env python3
"""
RAE Session Bootstrap Script (Smart Black Box Connector)
======================================================
MANDATORY STARTUP STEP.
Dependency-free version (uses standard library only).
Forces "RAE-First" by INJECTING active memory context directly into stdout.
"""

import sys
import json
import os
import urllib.request
import urllib.error
import socket

# --- Configuration ---
DEFAULT_URL = "http://localhost:8001"
LUMINA_URL = "http://100.68.166.117:8001"
LITE_URL = "http://localhost:8008"

# Standard headers
HEADERS = {
    "Content-Type": "application/json",
    "X-Tenant-Id": "default-tenant"
}

def make_request(url, method='GET', data=None, timeout=5):
    """Robust HTTP request using standard library."""
    try:
        if data:
            data_bytes = json.dumps(data).encode('utf-8')
        else:
            data_bytes = None

        req = urllib.request.Request(url, data=data_bytes, headers=HEADERS, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, {"error": str(e)}
    except urllib.error.URLError as e:
        return 0, {"error": str(e.reason)}
    except socket.timeout:
        return 0, {"error": "timeout"}
    except Exception as e:
        return 0, {"error": str(e)}

def get_active_url():
    """Finds the working RAE API URL."""
    print("🔍 Probing RAE Nodes...")
    urls = [DEFAULT_URL, LUMINA_URL, LITE_URL]
    
    for url in urls:
        print(f"   Target: {url} ... ", end="", flush=True)
        code, _ = make_request(f"{url}/health", timeout=1)
        if code == 200:
            print("ONLINE ✅")
            return url
        print("OFFLINE ❌")
    return None

def fetch_black_box_context(base_url):
    """Pulls the latest mental state from RAE."""
    print(f"\n🧠 ACCESSING HIVE MIND via {base_url}...")
    
    # 1. Fetch Working Memory (Immediate Context)
    query_payload = {
        "query_text": "Current session goals, active tasks, and recent critical fixes",
        "k": 5,
        "layers": ["working", "episodic"]
    }
    
    code, data = make_request(f"{base_url}/v1/memory/query", method='POST', data=query_payload)
    
    if code == 200:
        results = data.get("results", [])
        print("\n=== 📂 ACTIVE CONTEXT (FROM RAE) ===")
        if not results:
            print("(No recent context found. Starting fresh?)")
        for item in results:
            content = item.get("content") or item.get("text")
            layer = item.get("layer", "unknown")
            print(f"[{layer.upper()}] {content[:200]}..." if len(content) > 200 else f"[{layer.upper()}] {content}")
    else:
        print(f"⚠️  Memory Query Failed: {code}")

    # 2. Fetch Strategic Directives (Reflective)
    query_payload["layers"] = ["reflective", "semantic"]
    query_payload["query_text"] = "Strategic protocols, critical stability rules"
    
    code, data = make_request(f"{base_url}/v1/memory/query", method='POST', data=query_payload)
    
    if code == 200:
        results = data.get("results", [])
        print("\n=== 🛡️  PROTOCOL DIRECTIVES ===")
        for item in results:
            content = item.get("content") or item.get("text")
            print(f"> {content}")

def log_session_start(base_url):
    """Automatically creates a memory trace that a new session has started."""
    import getpass
    import platform
    
    user = getpass.getuser()
    node = platform.node()
    
    payload = {
        "content": f"Session Bootstrap Initiated by {user} on {node}. Infrastructure Check: ONLINE.",
        "layer": "working",
        "importance": 0.1,
        "tags": ["session-start", "audit", "bootstrap"],
        "source": "bootstrap_script"
    }
    
    # Fire and forget (don't block startup if write fails, but try)
    try:
        make_request(f"{base_url}/v1/memory/store", method='POST', data=payload)
        # We don't print confirmation to keep stdout clean for the agent context, 
        # but the memory is stored.
    except:
        pass

def main():
    print("🔌 RAE-First Bootstrap (Zero-Dep Mode)...")
    
    active_url = get_active_url()
    
    if not active_url:
        print("\n❌ CRITICAL: RAE IS UNREACHABLE.")
        print("Infrastructure is broken. Agent must perform REPAIR.")
        print("1. Kill ghosts: ss -lptn 'sport = :8001'")
        print("2. Reset Docker: docker compose down && docker network prune -f && docker compose up -d rae-api-dev")
        print("3. Try Lumina: ssh operator@100.68.166.117")
        sys.exit(1)
    
    # Success path
    log_session_start(active_url)
    fetch_black_box_context(active_url)
    
    print("\n✅ SESSION READY. Proceed with RAE context.")

if __name__ == "__main__":
    main()
