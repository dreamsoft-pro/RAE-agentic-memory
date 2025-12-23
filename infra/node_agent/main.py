import asyncio
import logging
import os
import platform
import socket
import sys
import yaml
import httpx
from typing import Any, Dict, Optional

# Constants
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
DEFAULT_API_URL = "http://localhost:8000"

# Logging setup
# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOG_DIR, 'agent.log'))
    ]
)
logger = logging.getLogger("node_agent")

class NodeAgent:
    def __init__(self):
        self.config = self._load_config()
        self.node_id = self.config.get('node_id', socket.gethostname())
        self.api_key = self.config.get('api_key', 'dev-secret')
        self.base_url = self.config.get('rae_endpoint', DEFAULT_API_URL).rstrip('/')
        self.heartbeat_interval = self.config.get('heartbeat_interval_sec', 30)
        self.capabilities = self.config.get('capabilities', {})
        
        # Override capabilities with auto-detection if enabled
        if self.config.get('auto_detect_capabilities', True):
            self._detect_capabilities()

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        return {}

    def _detect_capabilities(self):
        """Detect system hardware and software."""
        self.capabilities['os'] = platform.system()
        self.capabilities['hostname'] = socket.gethostname()
        self.capabilities['cpu_count'] = os.cpu_count()
        self.capabilities['arch'] = platform.machine()
        
        # GPU Detection (NVIDIA)
        try:
            import subprocess
            smi_out = subprocess.check_output(['nvidia-smi', '-L'], text=True)
            self.capabilities['gpu'] = True
            self.capabilities['gpu_info'] = smi_out.strip()
            self.capabilities['vram_gb'] = 16 # Placeholder/Estimate or parse smi_out
        except Exception:
            self.capabilities['gpu'] = False

    async def register(self, client: httpx.AsyncClient):
        payload = {
            "node_id": self.node_id,
            "api_key": self.api_key,
            "capabilities": self.capabilities
        }
        try:
            url = f"{self.base_url}/control/nodes/register"
            logger.info(f"Registering at {url}...")
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            logger.info(f"Registered successfully as {self.node_id}")
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            # Don't raise, just retry later or run in degraded mode
            # Actually, without registration, we shouldn't proceed?
            # We'll retry in the loop.
            pass

    async def heartbeat_loop(self, client: httpx.AsyncClient):
        while True:
            try:
                payload = {"node_id": self.node_id, "status": "ONLINE"}
                await client.post(f"{self.base_url}/control/nodes/heartbeat", json=payload)
                logger.debug("Heartbeat sent")
            except Exception as e:
                logger.error(f"Heartbeat failed: {e}")
            
            await asyncio.sleep(self.heartbeat_interval)

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Processing task {task.get('id')} of type {task.get('type')}")
        # TODO: Implement actual task processing logic here
        # For now, simulation
        await asyncio.sleep(2)
        return {"status": "success", "output": "processed_by_node_v1"}

    async def task_loop(self, client: httpx.AsyncClient):
        poll_url = f"{self.base_url}/control/tasks/poll"
        while True:
            try:
                resp = await client.get(poll_url, params={"node_id": self.node_id})
                if resp.status_code == 200:
                    task = resp.json()
                    if task:
                        result = {}
                        error = None
                        try:
                            result = await self.process_task(task)
                        except Exception as e:
                            logger.error(f"Task execution failed: {e}")
                            error = str(e)
                        
                        # Submit result
                        submit_url = f"{self.base_url}/control/tasks/{task['id']}/result"
                        payload = {"task_id": task['id'], "result": result, "error": error}
                        await client.post(submit_url, json=payload)
                        logger.info(f"Task {task['id']} result submitted")
            except Exception as e:
                # logger.error(f"Task polling error: {e}")
                # Reduce noise
                pass
            
            await asyncio.sleep(2) # Normal poll interval

    async def run(self):
        async with httpx.AsyncClient(timeout=10.0) as client:
            await self.register(client)
            await asyncio.gather(
                self.heartbeat_loop(client),
                self.task_loop(client)
            )

if __name__ == "__main__":
    agent = NodeAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Agent stopping...")