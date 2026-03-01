import asyncio
import json
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def search_via_mcp():
    print("[*] Connecting to MCP Server at http://localhost:8001/sse...")
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # List tools to be sure
            tools = await session.list_tools()
            print(f"[*] Available tools: {[t.name for t in tools.tools]}")
            
            queries = ["Node1", "Code Factory", "how to delegate", "kubus-gpu-01"]
            for q in queries:
                print(f"\n--- Searching for: {q} ---")
                try:
                    result = await session.call_tool("search_memory", arguments={
                        "query": q,
                        "top_k": 5
                    })
                    for block in result.content:
                        if hasattr(block, 'text'):
                            print(block.text)
                        else:
                            print(block)
                except Exception as e:
                    print(f"Search failed for '{q}': {e}")

if __name__ == "__main__":
    try:
        asyncio.run(search_via_mcp())
    except Exception as e:
        print(f"Error: {e}")
