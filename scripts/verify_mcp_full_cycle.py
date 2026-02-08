import asyncio
import os

from rae_mcp.server import RAEMemoryClient

# Konfiguracja środowiska
os.environ["RAE_API_URL"] = "http://localhost:8001"
os.environ["RAE_API_KEY"] = "dev-key"
os.environ["RAE_TENANT_ID"] = "b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22"
os.environ["RAE_PROJECT_ID"] = "mcp-verification-project"

async def main():
    print("🚀 Starting MCP Full Cycle Verification (Layers & Vectors)...")

    client = RAEMemoryClient(
        api_url=os.environ["RAE_API_URL"],
        api_key=os.environ["RAE_API_KEY"],
        tenant_id=os.environ["RAE_TENANT_ID"]
    )

    created_ids = []

    # 1. ZAPIS DO RÓŻNYCH WARSTW
    layers_to_test = ["working", "episodic", "semantic"]
    print("\n📝 Step 1: Saving memories to multiple layers...")

    for layer in layers_to_test:
        content = f"MCP_TEST_VECTOR_LAYER_{layer.upper()}: This is a specific test memory for the {layer} layer to verify hybrid search stability."
        try:
            result = await client.store_memory(
                content=content,
                source="mcp-full-cycle-test",
                layer=layer,
                tags=["mcp-test", f"layer-{layer}"],
                project="mcp-verification-project",
                importance=0.9
            )
            mem_id = result.get("id")
            if mem_id:
                created_ids.append(mem_id)
                print(f"   ✅ Saved to {layer.ljust(10)} | ID: {mem_id}")
            else:
                print(f"   ❌ Failed to get ID for {layer}")
        except Exception as e:
            print(f"   ❌ Error saving to {layer}: {e}")

    # Czekamy chwilę na indeksację
    print("\n⏳ Waiting 2s for indexing...")
    await asyncio.sleep(2)

    # 2. WYSZUKIWANIE (HYBRID SEARCH)
    print("\n🔍 Step 2: Testing Hybrid Search across layers...")

    query = "MCP_TEST_VECTOR_LAYER verify stability"

    try:
        results = await client.search_memory(
            query=query,
            top_k=10,
            project="mcp-verification-project"
        )

        print(f"   Found {len(results)} results.")

        found_layers = set()
        for mem in results:
            layer = mem.get("layer") or mem.get("metadata", {}).get("layer") or "unknown"
            found_layers.add(layer)

            score = mem.get("score", 0.0)
            content_snippet = mem.get("content", "")[:60]
            print(f"   - [{score:.3f}] [{layer}] {content_snippet}...")

        missing_layers = set(layers_to_test) - found_layers
        if not missing_layers:
            print("\n   ✅ SUCCESS: Found memories from ALL tested layers.")
        else:
            print(f"\n   ⚠️ WARNING: Missing results from layers: {missing_layers}")

    except Exception as e:
        print(f"   ❌ Search failed (Vector Dimension Mismatch?): {e}")

    # 3. USUNIĘCIE (CLEANUP)
    print("\n🧹 Step 3: Cleanup...")
    import httpx
    async with httpx.AsyncClient() as http:
        for mem_id in created_ids:
            try:
                resp = await http.delete(
                    f"http://localhost:8001/v2/memories/{mem_id}",
                    headers={"X-Tenant-Id": os.environ["RAE_TENANT_ID"]}
                )
                if resp.status_code == 200:
                    print(f"   ✅ Deleted {mem_id}")
                else:
                    print(f"   ⚠️ Failed to delete {mem_id}: {resp.status_code}")
            except Exception as e:
                print(f"   ⚠️ Error deleting {mem_id}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
