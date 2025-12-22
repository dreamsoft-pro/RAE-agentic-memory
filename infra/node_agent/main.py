import asyncio
import logging
import os
import platform
import socket
from typing import Any, Dict

import httpx

# Configuration
RAE_API_URL = os.getenv("RAE_API_URL", "http://localhost:8000") # Default to local for testing
NODE_ID = os.getenv("NODE_ID", platform.node()) # Default to hostname
API_KEY = os.getenv("NODE_API_KEY", "dev-secret")
HEARTBEAT_INTERVAL = 30
POLL_INTERVAL = 5

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("node_agent")

async def get_system_capabilities() -> Dict[str, Any]:
    # TODO: Detect GPU, RAM, etc.
    return {
        "os": platform.system(),
        "hostname": socket.gethostname(),
        "cpu_count": os.cpu_count(),
        "gpu": False # Placeholder
    }

async def register(client: httpx.AsyncClient):
    caps = await get_system_capabilities()
    payload = {
        "node_id": NODE_ID,
        "api_key": API_KEY,
        "capabilities": caps
    }
    try:
        resp = await client.post(f"{RAE_API_URL}/control/nodes/register", json=payload)
        resp.raise_for_status()
        logger.info(f"Registered successfully as {NODE_ID}")
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise

async def heartbeat_loop(client: httpx.AsyncClient):
    while True:
        try:
            payload = {"node_id": NODE_ID, "status": "ONLINE"}
            await client.post(f"{RAE_API_URL}/control/nodes/heartbeat", json=payload)
            logger.debug("Heartbeat sent")
        except Exception as e:
            logger.error(f"Heartbeat failed: {e}")

        await asyncio.sleep(HEARTBEAT_INTERVAL)

async def process_task(task: Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f"Processing task {task['id']} of type {task['type']}")
    # Simulate work
    await asyncio.sleep(1)
    return {"status": "success", "output": "processed"}

async def task_loop(client: httpx.AsyncClient):
    while True:
        try:
            # Poll for task
            resp = await client.get(f"{RAE_API_URL}/control/tasks/poll", params={"node_id": NODE_ID})
            if resp.status_code == 200 and resp.json():
                task = resp.json()
                try:
                    result = await process_task(task)
                    # Submit result
                    await client.post(
                        f"{RAE_API_URL}/control/tasks/{task['id']}/result",
                        json={"task_id": task['id'], "result": result}
                    )
                    logger.info(f"Task {task['id']} completed")
                except Exception as e:
                    logger.error(f"Task processing failed: {e}")
                    await client.post(
                        f"{RAE_API_URL}/control/tasks/{task['id']}/result",
                        json={"task_id": task['id'], "result": {}, "error": str(e)}
                    )
            else:
                # No task, sleep
                pass
        except Exception as e:
             logger.error(f"Task polling error: {e}")

        await asyncio.sleep(POLL_INTERVAL)

async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Initial registration
        await register(client)

        # Start loops
        await asyncio.gather(
            heartbeat_loop(client),
            task_loop(client)
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Agent stopping...")
