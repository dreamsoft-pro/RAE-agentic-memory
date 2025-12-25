import logging
import asyncio
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from ..models import LLMRequest, LLMResponse, TokenUsage
from .base import LLMProvider

logger = logging.getLogger(__name__)

class DelegatedLLMProvider(LLMProvider):
    """
    LLM Provider that delegates inference to a remote compute node via Task Queue.
    """

    def __init__(self, task_repo: Any, timeout_sec: int = 120):
        """
        Initialize with a task repository (or raw connection pool).
        """
        self.task_repo = task_repo
        self.timeout_sec = timeout_sec
        self.name = "delegated"
        self.max_context_tokens = 32768
        self.supports_streaming = False
        self.supports_tools = False

    async def complete(self, request: LLMRequest) -> LLMResponse:
        """
        Create a delegation task and wait for the result.
        """
        # 1. Create task
        task_payload = {
            "model": request.model,
            "prompt": request.prompt,
            "system": request.system or "",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "goal": "Generate LLM completion"
        }
        
        # Resolve repository
        from apps.memory_api.repositories.task_repository import TaskRepository
        if not isinstance(self.task_repo, TaskRepository):
             repo = TaskRepository(self.task_repo)
        else:
             repo = self.task_repo

        task = await repo.create_task(
            type="llm_inference",
            payload=task_payload,
            priority=request.priority or 10
        )
        
        task_id = task.id
        logger.info(f"LLM task delegated: {task_id} (model: {request.model})")
        
        # 2. Poll for result
        import time
        start_time = time.time()
        while time.time() - start_time < self.timeout_sec:
            updated_task = await repo.get_task(task_id)
            if updated_task and updated_task.status == "COMPLETED":
                import json
                result_data = updated_task.result
                if isinstance(result_data, str):
                    result_data = json.loads(result_data)
                
                # result_data expected format: {"response": "..."} (Ollama format in node agent)
                text = result_data.get("response", "")
                
                return LLMResponse(
                    text=text,
                    usage=TokenUsage(
                        prompt_tokens=0, completion_tokens=0, total_tokens=0
                    ),
                    model_name=request.model,
                    finish_reason="stop",
                    raw=result_data
                )
            elif updated_task and updated_task.status == "FAILED":
                raise RuntimeError(f"Delegated LLM task {task_id} failed: {updated_task.error}")
            
            await asyncio.sleep(1.0)
            
        raise TimeoutError(f"Delegated LLM task {task_id} timed out after {self.timeout_sec}s")
