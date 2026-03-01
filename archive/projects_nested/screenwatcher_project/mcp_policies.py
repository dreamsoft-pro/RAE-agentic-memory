import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def list_policies():
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            print("Listing policies via MCP...")
            result = await session.call_tool("list_policies", arguments={})
            for block in result.content:
                print(block.text)

if __name__ == "__main__":
    asyncio.run(list_policies())
