import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def related_context():
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            queries = ["Node1 kubus-gpu-01 delegation", "code factory task type", "how to use node1"]
            for q in queries:
                print(f"\n--- Related Context for: {q} ---")
                try:
                    res = await session.call_tool("get_related_context", arguments={"query": q})
                    for block in res.content:
                        print(block.text)
                except Exception as e:
                    print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(related_context())
