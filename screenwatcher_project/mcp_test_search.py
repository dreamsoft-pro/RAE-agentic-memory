import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def test_search():
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Content from save_state.py
            q = "Iteration 11 complete Edge Client EXEs"
            print(f"--- Querying for known state: {q} ---")
            res = await session.call_tool("search_memory", arguments={"query": q, "top_k": 5})
            for block in res.content:
                print(block.text)

if __name__ == "__main__":
    asyncio.run(test_search())
