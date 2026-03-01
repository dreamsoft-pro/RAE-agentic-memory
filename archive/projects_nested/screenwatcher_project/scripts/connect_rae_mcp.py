#!/usr/bin/env python3
import subprocess
import json
import sys

# Configuration
CONTAINER_NAME = "rae-api-dev"
TENANT_ID = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11" # screenwatcher
MCP_PORT = 8000 # Internal port in container
PROJECT_NAME = "screenwatcher_project"

def run_in_container(python_code):
    """Executes Python code inside the RAE container where 'mcp' lib exists."""
    cmd = [
        "docker", "exec", "-i", CONTAINER_NAME, 
        "python3", "-c", python_code
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Container Execution Error:\n{result.stderr}")
        return None
    return result.stdout.strip()

def fetch_context():
    """Fetches recent memories via RAE MCP/API."""
    print(f"🔌 Connecting to RAE (Tenant: {TENANT_ID})...")
    
    code = f"""
import asyncio
import json
import sys

# Mocking MCP client logic via direct internal API call since we are inside the container
# OR using httpx/curl if mcp client lib is complex to script inline.
# For robustness, we use the REST API which backs the MCP.

import http.client

def get_memories():
    conn = http.client.HTTPConnection("localhost", {MCP_PORT})
    headers = {{
        "X-Tenant-Id": "{TENANT_ID}",
        "Content-Type": "application/json"
    }}
    # Get last 5 memories
    conn.request("GET", "/v1/memory/list?limit=5", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    return data

print(get_memories())
"""
    output = run_in_container(code)
    if not output:
        return
    
    try:
        memories = json.loads(output)
        print("\n🧠 RAE Context (Last 5 Memories):")
        if isinstance(memories, list):
            for mem in memories:
                # Handle different memory formats
                content = mem.get("content") or mem.get("text") or str(mem)
                print(f" - {content[:100]}...")
        else:
            print(output)
    except json.JSONDecodeError:
        print(f"Raw Output: {output}")

def register_session():
    """Logs session start to RAE."""
    print("📝 Registering Session Start...")
    code = f"""
import http.client
import json

def log_start():
    conn = http.client.HTTPConnection("localhost", {MCP_PORT})
    headers = {{
        "X-Tenant-Id": "{TENANT_ID}",
        "Content-Type": "application/json"
    }}
    body = {{
        "project": "{PROJECT_NAME}",
        "layer": "episodic",
        "content": "Agent Session Started via CLI Wrapper",
        "source": "gemini_cli",
        "metadata": {{ "type": "session_start" }}
    }}
    conn.request("POST", "/v1/memory/store", json.dumps(body), headers=headers)
    res = conn.getresponse()
    print(res.status)
    conn.close()

log_start()
"""
    run_in_container(code)

if __name__ == "__main__":
    fetch_context()
    register_session()
