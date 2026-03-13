import asyncio
import os
import subprocess
import sys
from datetime import datetime

# Importy z biblioteki MCP (zakładamy uruchomienie w venv gdzie jest zainstalowana)
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

MCP_URL = "http://localhost:9001/sse"
PROJECT_NAME = "screenwatcher_project"

def get_git_status():
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            return "Git status: Error"
        
        changes = result.stdout.strip()
        if not changes:
            return "Git status: Clean"
        
        lines = changes.split('\n')
        summary = f"Git status: {len(lines)} changed files"
        return summary
    except Exception:
        return "Git status: Unknown (git not found)"

async def boot_sequence():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Initiating Boot Sequence via RAE MCP...")
    
    try:
        async with sse_client(MCP_URL) as streams:
            read_stream, write_stream = streams
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # 1. Rejestracja startu sesji
                print("📝 Registering session start...", end=" ")
                start_msg = f"Session started. OS: {sys.platform}. {get_git_status()}"
                
                await session.call_tool("save_memory", arguments={
                    "content": start_msg,
                    "source": "boot_script",
                    "tag": "session_start",
                    "layer": "episodic"
                })
                print("✅ Done.")

                # 2. Pobranie kontekstu (ostatnie wspomnienia)
                print("🧠 Fetching context...", end=" ")
                context_result = await session.call_tool("search_memory", arguments={
                    "query": "current task context plan",
                    "top_k": 3
                })
                print("✅ Received.")
                
                # Wyświetlenie skondensowanego kontekstu dla Agenta
                print("\n--- 📂 RAE CONTEXT SUMMARY ---")
                # Zakładamy, że narzędzie zwraca tekst (TextContent)
                content_blocks = context_result.content
                for block in content_blocks:
                    if block.type == "text":
                        print(block.text)
                print("------------------------------\n")

    except Exception as e:
        print(f"\n❌ CRITICAL: Failed to connect to RAE via MCP: {e}")
        print("Make sure the MCP server is running (tools/rae_mcp/start_server.bat)")

if __name__ == "__main__":
    asyncio.run(boot_sequence())
