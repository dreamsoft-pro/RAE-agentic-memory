import asyncio
import os
import sys
from rae_mcp.server import RAEMemoryClient

# Konfiguracja środowiska (symulacja zmiennych z MCP)
os.environ["RAE_API_URL"] = "http://localhost:8001"
os.environ["RAE_API_KEY"] = "dev-key"
os.environ["RAE_TENANT_ID"] = "b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22" # Tenant ID z bazy
os.environ["RAE_PROJECT_ID"] = "test-project"

async def main():
    print("🚀 Starting MCP Client Verification...")
    
    # Inicjalizacja klienta (użyje zaktualizowanego kodu z V2)
    client = RAEMemoryClient(
        api_url=os.environ["RAE_API_URL"],
        api_key=os.environ["RAE_API_KEY"],
        tenant_id=os.environ["RAE_TENANT_ID"]
    )
    
    # 1. Zapis pamięci
    print("\n📝 Testing store_memory...")
    try:
        content = "MCP_PYTHON_CLIENT_TEST: Weryfikacja klienta Python po migracji na V2."
        result = await client.store_memory(
            content=content,
            source="python-script",
            layer="working",
            tags=["python-client", "v2-verify"],
            project="test-project",
            importance=0.8
        )
        memory_id = result.get("id")
        print(f"✅ Memory stored! ID: {memory_id}")
    except Exception as e:
        print(f"❌ store_memory failed: {e}")
        return

    # 2. Wyszukiwanie pamięci (Hybrid Search)
    print("\n🔍 Testing search_memory (Hybrid Search)...")
    try:
        results = await client.search_memory(
            query="MCP_PYTHON_CLIENT_TEST",
            top_k=5,
            project="test-project"
        )
        
        if results:
            print(f"✅ Found {len(results)} memories.")
            for mem in results:
                score = mem.get('score', 0.0)
                content_snippet = mem.get('content', '')[:50]
                mem_id = mem.get('id')
                print(f"   - [{score:.2f}] {content_snippet}...")
                
                # Porównanie ID (uwaga: w wynikach search może być 'id' lub 'memory_id')
                if mem_id == memory_id:
                    print("     (Confirmed: Found the just-created memory)")
        else:
            print("⚠️ No results found immediately (indexing lag?).")
            
    except Exception as e:
        print(f"❌ search_memory failed: {e}")

    # 3. Usunięcie (Cleanup)
    if 'memory_id' in locals() and memory_id:
        print("\n🧹 Cleaning up...")
        import httpx
        async with httpx.AsyncClient() as http:
            try:
                resp = await http.delete(
                    f"http://localhost:8001/v2/memories/{memory_id}",
                    headers={"X-Tenant-Id": os.environ["RAE_TENANT_ID"]}
                )
                if resp.status_code == 200:
                    print("✅ Memory deleted.")
                else:
                    print(f"⚠️ Cleanup failed: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")

if __name__ == "__main__":
    asyncio.run(main())