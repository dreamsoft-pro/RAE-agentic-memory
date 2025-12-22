import json
from typing import Any, Dict, Optional
from uuid import UUID

import asyncpg

from apps.memory_api.models.control_plane import DelegatedTask, TaskStatus


class TaskRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create_task(
        self, type: str, payload: Dict[str, Any], priority: int = 0
    ) -> DelegatedTask:
        record = await self.pool.fetchrow(
            """
            INSERT INTO delegated_tasks (type, payload, priority, status)
            VALUES ($1, $2, $3, 'PENDING')
            RETURNING *
            """,
            type,
            json.dumps(payload),
            priority,
        )
        data = dict(record)
        if isinstance(data.get("payload"), str):
            data["payload"] = json.loads(data["payload"])
        if isinstance(data.get("result"), str):
            data["result"] = json.loads(data["result"])
        return DelegatedTask(**data)

    async def claim_task(self, node_id: UUID) -> Optional[DelegatedTask]:
        # Atomic claim: Select pending task with highest priority, lock it, update it.
        # Postgres supports LIMIT 1 FOR UPDATE SKIP LOCKED
        record = await self.pool.fetchrow(
            """
            UPDATE delegated_tasks
            SET status = 'PROCESSING', assigned_node_id = $1, started_at = NOW()
            WHERE id = (
                SELECT id
                FROM delegated_tasks
                WHERE status = 'PENDING'
                ORDER BY priority DESC, created_at ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED
            )
            RETURNING *
            """,
            node_id,
        )
        if record:
            data = dict(record)
            if isinstance(data.get("payload"), str):
                data["payload"] = json.loads(data["payload"])
            if isinstance(data.get("result"), str):
                data["result"] = json.loads(data["result"])
            return DelegatedTask(**data)
        return None

    async def complete_task(
        self, task_id: UUID, result: Dict[str, Any], error: Optional[str] = None
    ) -> Optional[DelegatedTask]:
        status = TaskStatus.FAILED if error else TaskStatus.COMPLETED
        record = await self.pool.fetchrow(
            """
            UPDATE delegated_tasks
            SET status = $2, result = $3, error = $4, completed_at = NOW()
            WHERE id = $1
            RETURNING *
            """,
            task_id,
            status.value,
            json.dumps(result),
            error,
        )
        if record:
            data = dict(record)
            if isinstance(data.get("payload"), str):
                data["payload"] = json.loads(data["payload"])
            if isinstance(data.get("result"), str):
                data["result"] = json.loads(data["result"])
            return DelegatedTask(**data)
        return None
