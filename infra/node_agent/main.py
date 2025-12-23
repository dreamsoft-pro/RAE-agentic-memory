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
        task_type = task.get('type')
        payload = task.get('payload', {})
        logger.info(f"Processing task {task.get('id')} of type {task_type}")
        
        if task_type == "llm_inference":
            return await self._execute_ollama(payload)
        elif task_type in ["code_verify_cycle", "quality_loop"]:
            return await self._execute_code_cycle(payload)
        
        return {"status": "success", "output": "unknown_task_type"}

    async def _execute_code_cycle(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Writer/Reviewer cycle for high quality code."""
        writer_model = payload.get("writer_model", "deepseek-coder:33b")
        reviewer_model = payload.get("reviewer_model", "deepseek-coder:6.7b")
        instruction = payload.get("prompt") or payload.get("task", "")
        diff = payload.get("diff", "")
        
        # Forceful prompt construction to ensure DeepSeek analyzes the actual code
        write_prompt = (
            "### INSTRUCTION\n"
            f"{instruction}\n\n"
            "### CODE TO ANALYZE (DIFF)\n"
            f"```diff\n{diff}\n```\n\n"
            "### TASK\n"
            "Analyze the DIFF above. Identify any violations of agnosticism, security risks, or logic errors. "
            "Provide specific feedback or a corrected version of the code if necessary."
        )

        # 1. WRITE (Analysis/Drafting)
        logger.info(f"Phase 1: Writing analysis/code with {writer_model}")
        write_result = await self._call_ollama(writer_model, write_prompt)
        if write_result["status"] == "error": return write_result
        initial_output = write_result["response"]

        # 2. REVIEW
        logger.info(f"Phase 2: Reviewing output with {reviewer_model}")
        review_prompt = (
            "You are a Senior Python Architect. Review the following analysis/code review for correctness and depth. "
            "Check if the reviewer actually looked at the provided diff. "
            "If the analysis is accurate and complete, respond ONLY with 'PASSED'. "
            "Otherwise, point out what was missed in the diff.\n\n"
            f"ANALYSIS TO REVIEW:\n{initial_output}"
        )


    async def _call_ollama(self, model: str, prompt: str, system: str = "") -> Dict[str, Any]:
        ollama_url = self.config.get("ollama_api_url", "http://localhost:11434")
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                resp = await client.post(f"{ollama_url}/api/generate", json={
                    "model": model, "prompt": prompt, "system": system, "stream": False
                })
                resp.raise_for_status()
                return {"status": "success", "response": resp.json().get("response")}
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def _execute_ollama(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_ollama(
            payload.get("model", "deepseek-coder:33b"),
            payload.get("prompt", ""),
            payload.get("system", "")
        )

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