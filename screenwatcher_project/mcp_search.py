import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def search_via_mcp():
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            print("Searching for 'Node1' via MCP...")
            result = await session.call_tool("search_memory", arguments={
                "query": "Node1 workflow DeepSeek Ollama",
                "top_k": 5
            })
            
            for block in result.content:
                if block.type == "text":
                    print(block.text)

if __name__ == "__main__":
    try:
        asyncio.run(search_via_mcp())
    except Exception as e:
        print(f"Error: {e}")
