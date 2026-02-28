import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def test_mcp_project():
    async with sse_client("http://localhost:8001/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Save
            print("Saving test memory...")
            await session.call_tool("save_memory", arguments={
                "content": "SECRET_KEY_FOR_NODE1: DEEPSEEK_OLLAMA_WORKFLOW",
                "project": "screenwatcher_project",
                "tag": "test_tag",
                "layer": "semantic"
            })
            
            # Search
            print("Searching for test memory...")
            res = await session.call_tool("search_memory", arguments={
                "query": "SECRET_KEY_FOR_NODE1",
                "project": "screenwatcher_project",
                "top_k": 1
            })
            
            for block in res.content:
                print(f"Result: {block.text}")

if __name__ == "__main__":
    asyncio.run(test_mcp_project())
