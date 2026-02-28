import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def deep_search():
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            queries = [
                "how to delegate to Node1",
                "Node1 task type",
                "DeepSeek Ollama workflow",
                "kubus-gpu-01 protocol",
                "POST /control/tasks example"
            ]
            
            for q in queries:
                print(f"--- Query: {q} ---")
                res = await session.call_tool("search_memory", arguments={"query": q, "top_k": 5})
                for block in res.content:
                    print(block.text)

if __name__ == "__main__":
    asyncio.run(deep_search())
