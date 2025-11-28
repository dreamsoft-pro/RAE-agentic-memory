"""
Memory Maintenance Workers - Async Tasks for Decay and Summarization

This module implements background tasks for:
1. Memory importance decay
2. Session summarization
3. Light "dreaming" (batch reflections)

These tasks should be run periodically (cron, scheduler, or task queue).
"""

import asyncio
from datetime import datetime, timedelta, timezone
from time import time
from typing import Any, Dict, List, Optional
from uuid import UUID

import asyncpg
import structlog

from apps.memory_api.config import settings
from apps.memory_api.metrics import (
    rae_reflective_decay_duration_seconds,
    rae_reflective_decay_updated_total,
)
from apps.memory_api.repositories.memory_repository import MemoryRepository
from apps.memory_api.services.importance_scoring import ImportanceScoringService
from apps.memory_api.services.reflection_engine_v2 import (
    Event,
    EventType,
    OutcomeType,
    ReflectionContext,
    ReflectionEngineV2,
)

logger = structlog.get_logger(__name__)


# ============================================================================
# Decay Worker
# ============================================================================


class DecayWorker:
    """
    Worker for applying time-based importance decay to memories.

    Runs periodically (e.g., daily) to reduce importance of stale memories.
    """

    def __init__(
        self,
        pool: asyncpg.Pool,
        scoring_service: Optional[ImportanceScoringService] = None,
    ):
        self.pool = pool
        self.scoring_service = scoring_service or ImportanceScoringService(db=pool)

    async def run_decay_cycle(
        self,
        tenant_ids: Optional[List[str]] = None,
        decay_rate: float = 0.01,
        consider_access_stats: bool = True,
    ) -> Dict[str, int]:
        """
        Run a decay cycle for all tenants or specified tenants.

        Args:
            tenant_ids: Optional list of tenant IDs (None = all tenants)
            decay_rate: Base decay rate (default 0.01 = 1% per day)
            consider_access_stats: Use access stats for decay calculation

        Returns:
            Statistics about decay operation
        """
        start_time = time()

        logger.info(
            "decay_cycle_started",
            tenant_count=len(tenant_ids) if tenant_ids else "all",
            decay_rate=decay_rate,
            consider_access_stats=consider_access_stats,
        )

        # Get tenant list if not provided
        if tenant_ids is None:
            tenant_ids = await self._get_all_tenant_ids()

        stats = {"total_tenants": len(tenant_ids), "total_updated": 0}

        # Process each tenant
        for tenant_id in tenant_ids:
            try:
                tenant_start_time = time()

                updated_count = await self.scoring_service.decay_importance(
                    tenant_id=UUID(tenant_id),
                    decay_rate=decay_rate,
                    consider_access_stats=consider_access_stats,
                )
                stats["total_updated"] += updated_count

                # Record metrics
                rae_reflective_decay_updated_total.labels(tenant_id=tenant_id).inc(
                    updated_count
                )
                rae_reflective_decay_duration_seconds.labels(
                    tenant_id=tenant_id
                ).observe(time() - tenant_start_time)

                logger.info(
                    "tenant_decay_completed",
                    tenant_id=tenant_id,
                    updated_count=updated_count,
                    duration_seconds=time() - tenant_start_time,
                )

            except Exception as e:
                logger.error(
                    "tenant_decay_failed",
                    tenant_id=tenant_id,
                    error=str(e),
                    exc_info=True,
                )
                continue

        duration = time() - start_time
        logger.info(
            "decay_cycle_completed",
            stats=stats,
            total_duration_seconds=duration,
        )
        return stats

    async def _get_all_tenant_ids(self) -> List[str]:
        """Get all unique tenant IDs from memories table"""
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                "SELECT DISTINCT tenant_id FROM memories WHERE tenant_id IS NOT NULL"
            )
            return [str(r["tenant_id"]) for r in records]


# ============================================================================
# Summarization Worker
# ============================================================================


class SummarizationWorker:
    """
    Worker for creating session summaries from episodic memories.

    Runs after sessions complete or periodically for long sessions.
    """

    def __init__(
        self,
        pool: asyncpg.Pool,
        memory_repository: Optional[MemoryRepository] = None,
    ):
        self.pool = pool
        self.memory_repo = memory_repository or MemoryRepository(pool)

    async def summarize_session(
        self,
        tenant_id: str,
        project_id: str,
        session_id: UUID,
        min_events: int = 10,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a summary for a specific session.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            session_id: Session identifier
            min_events: Minimum events required for summarization

        Returns:
            Summary record dict or None if not enough events
        """
        # Check if summarization is enabled
        if not settings.SUMMARIZATION_ENABLED:
            logger.info(
                "session_summarization_skipped",
                tenant_id=tenant_id,
                reason="summarization_disabled",
            )
            return None

        logger.info(
            "session_summarization_started",
            tenant_id=tenant_id,
            project_id=project_id,
            session_id=str(session_id),
            min_events=settings.SUMMARIZATION_MIN_EVENTS,
        )

        # Get episodic memories for session
        # TODO: Add session_id filter once migration is applied
        episodic_memories = await self.memory_repo.get_episodic_memories(
            tenant_id=tenant_id, project=project_id, limit=100
        )

        if len(episodic_memories) < min_events:
            logger.info(
                "session_summarization_skipped",
                tenant_id=tenant_id,
                session_id=str(session_id),
                reason="insufficient_events",
                event_count=len(episodic_memories),
            )
            return None

        # Create summary content
        summary_content = self._create_summary_text(episodic_memories)

        # Calculate importance (higher for summaries)
        avg_importance = sum(m.get("importance", 0.5) for m in episodic_memories) / len(
            episodic_memories
        )
        summary_importance = min(avg_importance * 1.2, 1.0)

        # Store summary as episodic memory with special tag
        summary_record = await self.memory_repo.insert_memory(
            tenant_id=tenant_id,
            content=summary_content,
            source="summarization_worker",
            importance=summary_importance,
            layer="em",
            tags=["session_summary", "auto_generated"],
            timestamp=datetime.now(timezone.utc),
            project=project_id,
        )

        logger.info(
            "session_summarization_completed",
            tenant_id=tenant_id,
            session_id=str(session_id),
            summary_id=summary_record["id"],
            source_events=len(episodic_memories),
        )

        return summary_record

    def _create_summary_text(self, memories: List[Dict[str, Any]]) -> str:
        """
        Create summary text from memory list.

        In production, this would use LLM. For now, simple aggregation.
        """
        # Extract key facts
        contents = [m.get("content", "") for m in memories]

        # Simple summary (in production, use LLM)
        summary = f"Session summary ({len(memories)} events): "
        summary += " | ".join(contents[:5])  # First 5 events

        if len(contents) > 5:
            summary += f" ... and {len(contents) - 5} more events"

        return summary

    async def summarize_long_sessions(
        self,
        tenant_id: str,
        project_id: str,
        event_threshold: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Find and summarize long-running sessions.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            event_threshold: Minimum events to trigger summarization

        Returns:
            List of created summary records
        """
        logger.info(
            "long_session_summarization_started",
            tenant_id=tenant_id,
            project_id=project_id,
            threshold=event_threshold,
        )

        # TODO: Implement session detection and batch summarization
        # For now, return empty
        summaries = []

        logger.info(
            "long_session_summarization_completed",
            tenant_id=tenant_id,
            summaries_created=len(summaries),
        )

        return summaries


# ============================================================================
# Dreaming Worker (Light Reflection from History)
# ============================================================================


class DreamingWorker:
    """
    Worker for generating reflections from historical memory patterns.

    Implements "light dreaming" - periodic analysis of memory to find
    patterns, repeated errors, and generate high-level strategies.
    """

    def __init__(
        self,
        pool: asyncpg.Pool,
        reflection_engine: Optional[ReflectionEngineV2] = None,
        memory_repository: Optional[MemoryRepository] = None,
    ):
        self.pool = pool
        self.reflection_engine = reflection_engine or ReflectionEngineV2(pool)
        self.memory_repo = memory_repository or MemoryRepository(pool)

    async def run_dreaming_cycle(
        self,
        tenant_id: str,
        project_id: str,
        lookback_hours: int = 24,
        min_importance: float = 0.6,
        max_samples: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Run a dreaming cycle: analyze recent high-importance memories
        and generate meta-reflections.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            lookback_hours: Hours to look back
            min_importance: Minimum importance to consider
            max_samples: Maximum memories to sample

        Returns:
            List of generated reflection IDs
        """
        # Check if reflective memory and dreaming are enabled
        if not settings.REFLECTIVE_MEMORY_ENABLED or not settings.DREAMING_ENABLED:
            logger.info(
                "dreaming_cycle_skipped",
                tenant_id=tenant_id,
                reason="disabled_by_config",
                reflective_enabled=settings.REFLECTIVE_MEMORY_ENABLED,
                dreaming_enabled=settings.DREAMING_ENABLED,
            )
            return []

        logger.info(
            "dreaming_cycle_started",
            tenant_id=tenant_id,
            project_id=project_id,
            lookback_hours=lookback_hours,
            mode=settings.REFLECTIVE_MEMORY_MODE,
        )

        # Get high-importance episodic memories from recent period
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)

        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, content, importance, created_at, tags, metadata
                FROM memories
                WHERE tenant_id = $1
                  AND project = $2
                  AND layer = 'em'
                  AND importance >= $3
                  AND created_at >= $4
                ORDER BY importance DESC, created_at DESC
                LIMIT $5
                """,
                tenant_id,
                project_id,
                min_importance,
                cutoff_time,
                max_samples,
            )

        if len(records) < 3:
            logger.info(
                "dreaming_cycle_skipped",
                tenant_id=tenant_id,
                reason="insufficient_memories",
                count=len(records),
            )
            return []

        logger.info(
            "dreaming_analyzing_memories",
            tenant_id=tenant_id,
            memory_count=len(records),
        )

        # Convert to Event objects for reflection context
        events = []
        for i, rec in enumerate(records):
            event = Event(
                event_id=f"dream_event_{i}",
                event_type=EventType.SYSTEM_EVENT,
                timestamp=rec["created_at"],
                content=rec["content"],
                metadata={"importance": rec["importance"], "tags": rec.get("tags", [])},
            )
            events.append(event)

        # Create reflection context
        context = ReflectionContext(
            events=events,
            outcome=OutcomeType.PARTIAL,  # Dreaming is exploratory
            task_description="Analyzing patterns in recent high-importance memories",
            task_goal="Identify recurring themes, potential strategies, and meta-insights",
            tenant_id=tenant_id,
            project_id=project_id,
        )

        # Generate reflection
        try:
            result = await self.reflection_engine.generate_reflection(context)

            # Store reflection
            stored_ids = await self.reflection_engine.store_reflection(
                result=result,
                tenant_id=tenant_id,
                project_id=project_id,
            )

            logger.info(
                "dreaming_cycle_completed",
                tenant_id=tenant_id,
                reflection_id=stored_ids.get("reflection_id"),
                strategy_generated=stored_ids.get("strategy_id") is not None,
            )

            return [stored_ids]

        except Exception as e:
            logger.error(
                "dreaming_cycle_failed",
                tenant_id=tenant_id,
                error=str(e),
                exc_info=True,
            )
            return []


# ============================================================================
# Main Maintenance Scheduler
# ============================================================================


class MaintenanceScheduler:
    """
    Main scheduler coordinating all maintenance workers.

    This can be run as a standalone process or integrated with
    cron/systemd timers.
    """

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.decay_worker = DecayWorker(pool)
        self.summarization_worker = SummarizationWorker(pool)
        self.dreaming_worker = DreamingWorker(pool)

    async def run_daily_maintenance(
        self, tenant_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run daily maintenance tasks.

        Respects configuration flags:
        - REFLECTIVE_MEMORY_ENABLED: Master switch for all reflective operations
        - DREAMING_ENABLED: Controls dreaming worker
        - SUMMARIZATION_ENABLED: Controls summarization worker

        Args:
            tenant_ids: Optional list of tenant IDs (None = all)

        Returns:
            Statistics about maintenance operations
        """
        logger.info(
            "daily_maintenance_started",
            timestamp=datetime.now(timezone.utc),
            reflective_enabled=settings.REFLECTIVE_MEMORY_ENABLED,
            mode=settings.REFLECTIVE_MEMORY_MODE,
            dreaming_enabled=settings.DREAMING_ENABLED,
            summarization_enabled=settings.SUMMARIZATION_ENABLED,
        )

        stats = {
            "decay": {},
            "summarization": {},
            "dreaming": {},
            "started_at": datetime.now(timezone.utc).isoformat(),
            "config": {
                "reflective_enabled": settings.REFLECTIVE_MEMORY_ENABLED,
                "mode": settings.REFLECTIVE_MEMORY_MODE,
                "dreaming_enabled": settings.DREAMING_ENABLED,
                "summarization_enabled": settings.SUMMARIZATION_ENABLED,
            },
        }

        try:
            # 1. Run decay cycle (always runs for memory lifecycle management)
            logger.info("running_decay_cycle")
            stats["decay"] = await self.decay_worker.run_decay_cycle(
                tenant_ids=tenant_ids,
                decay_rate=settings.MEMORY_BASE_DECAY_RATE,
                consider_access_stats=settings.MEMORY_ACCESS_COUNT_BOOST,
            )

            # 2. Run dreaming cycles for each tenant (only if enabled)
            if settings.REFLECTIVE_MEMORY_ENABLED and settings.DREAMING_ENABLED:
                if tenant_ids is None:
                    tenant_ids = await self.decay_worker._get_all_tenant_ids()

                dreaming_results = []
                for tenant_id in tenant_ids[:10]:  # Limit to 10 tenants per cycle
                    try:
                        # For simplicity, use default project
                        results = await self.dreaming_worker.run_dreaming_cycle(
                            tenant_id=tenant_id,
                            project_id="default",  # TODO: Get actual projects
                            lookback_hours=settings.DREAMING_LOOKBACK_HOURS,
                            min_importance=settings.DREAMING_MIN_IMPORTANCE,
                            max_samples=settings.DREAMING_MAX_SAMPLES,
                        )
                        dreaming_results.extend(results)
                    except Exception as e:
                        logger.error(
                            "dreaming_failed_for_tenant",
                            tenant_id=tenant_id,
                            error=str(e),
                        )
                        continue

                stats["dreaming"] = {
                    "tenants_processed": len(tenant_ids[:10]),
                    "reflections_generated": len(dreaming_results),
                }
            else:
                stats["dreaming"] = {"skipped": True, "reason": "disabled_by_config"}
                logger.info(
                    "dreaming_skipped",
                    reflective_enabled=settings.REFLECTIVE_MEMORY_ENABLED,
                    dreaming_enabled=settings.DREAMING_ENABLED,
                )

            logger.info("daily_maintenance_completed", stats=stats)

        except Exception as e:
            logger.error("daily_maintenance_failed", error=str(e), exc_info=True)
            stats["error"] = str(e)

        stats["completed_at"] = datetime.now(timezone.utc).isoformat()
        return stats

    async def run_hourly_maintenance(self) -> Dict[str, Any]:
        """Run hourly maintenance tasks (lighter than daily)"""
        logger.info("hourly_maintenance_started")

        stats = {
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

        # Hourly tasks are lighter - just session summarization for now
        # In production, implement active session detection

        stats["completed_at"] = datetime.now(timezone.utc).isoformat()
        return stats


# ============================================================================
# CLI Entry Point
# ============================================================================


async def run_maintenance_cli():
    """
    CLI entry point for running maintenance tasks.

    Usage:
        python -m apps.memory_api.workers.memory_maintenance
    """
    import os

    # Get database URL from env
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL not set")
        return

    # Create pool
    pool = await asyncpg.create_pool(database_url)

    try:
        # Create scheduler
        scheduler = MaintenanceScheduler(pool)

        # Run daily maintenance
        stats = await scheduler.run_daily_maintenance()

        print("Maintenance completed:")
        print(f"  Decay: {stats.get('decay', {})}")
        print(f"  Dreaming: {stats.get('dreaming', {})}")

    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(run_maintenance_cli())
