import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def save():
    try:
        async with sse_client('http://localhost:8001/sse') as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                await session.call_tool('save_memory', {
                    'content': 'Iteration 11 complete. Edge Client EXEs built with portable OCR support. Legacy DB integration implemented with dynamic routing and Edge configuration support. Native Windows starter script RUN_BACKEND.bat created. All changes pushed to GitHub main/develop.',
                    'layer': 'reflective',
                    'tag': 'task_completion'
                })
                print("State saved to RAE successfully.")
    except Exception as e:
        print(f"Failed to save state: {e}")

if __name__ == "__main__":
    asyncio.run(save())
