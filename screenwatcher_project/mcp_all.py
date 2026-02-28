import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def search_all():
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            print("Searching for everything via MCP...")
            res = await session.call_tool("search_memory", arguments={"query": " ", "top_k": 20})
            for block in res.content:
                print(block.text)

if __name__ == "__main__":
    asyncio.run(search_all())
