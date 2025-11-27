import asyncpg
import structlog

from apps.memory_api.celery_app import celery_app
from apps.memory_api.config import settings
from apps.memory_api.services.community_detection import CommunityDetectionService
from apps.memory_api.services.context_cache import rebuild_full_cache
from apps.memory_api.services.entity_resolution import EntityResolutionService
from apps.memory_api.services.graph_extraction import GraphExtractionService
from apps.memory_api.services.reflection_engine import ReflectionEngine

logger = structlog.get_logger(__name__)


# --- Helper to create a DB pool for tasks ---
# Celery tasks run in a separate process, so we need to manage the DB pool.
async def get_pool():
    return await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )


@celery_app.task
def generate_reflection_for_project(project: str, tenant_id: str):
    """
    Celery task to generate a reflection for a specific project.
    """
    import asyncio

    async def main():
        pool = await get_pool()
        engine = ReflectionEngine(pool)
        await engine.generate_reflection(project, tenant_id)
        await pool.close()

    asyncio.run(main())


@celery_app.task
def schedule_reflections():
    """
    Periodically finds projects with recent activity and schedules reflection tasks.
    """
    import asyncio

    async def main():
        pool = await get_pool()
        # Find unique project/tenant pairs with recent episodic memories
        # A real implementation would be more sophisticated.
        records = await pool.fetch(
            """
            SELECT DISTINCT project, tenant_id
            FROM memories
            WHERE layer = 'em' AND created_at > NOW() - INTERVAL '1 hour'
        """
        )
        for record in records:
            generate_reflection_for_project.delay(
                record["project"], record["tenant_id"]
            )
        await pool.close()

    asyncio.run(main())


@celery_app.task
def apply_memory_decay():
    """
    Periodically applies decay to memory strength and deletes expired memories.
    """
    import asyncio

    async def main():
        pool = await get_pool()
        # Apply decay
        await pool.execute(
            "UPDATE memories SET strength = strength * $1", settings.MEMORY_DECAY_RATE
        )
        # Delete expired memories
        await pool.execute(
            "DELETE FROM memories WHERE expires_at IS NOT NULL AND expires_at < NOW()"
        )
        await pool.close()

    asyncio.run(main())


@celery_app.task
def prune_old_memories():
    """
    Periodically deletes old episodic memories to manage data lifecycle.
    """
    import asyncio

    async def main():
        if settings.MEMORY_RETENTION_DAYS <= 0:
            return  # Pruning is disabled

        pool = await get_pool()
        try:
            interval = f"{settings.MEMORY_RETENTION_DAYS} days"
            # We only prune episodic memories, as semantic/reflective are meant to be long-term.
            result = await pool.execute(
                "DELETE FROM memories WHERE layer = 'em' AND created_at < NOW() - $1::interval",
                interval,
            )
            # A structured logger would be better here, but for now, print.
            print(f"Pruned old memories: {result}")
        finally:
            await pool.close()

    asyncio.run(main())


@celery_app.task
def rebuild_cache():
    """
    Celery task to perform a full rebuild of the context cache.
    """
    import asyncio

    asyncio.run(rebuild_full_cache())


@celery_app.task(bind=True, max_retries=3)
def extract_graph_lazy(
    self, memory_ids: list, tenant_id: str, use_mini_model: bool = True
):
    """
    Celery task to extract knowledge graph from memories in background.

    This is the "lazy" extraction mode that saves costs by:
    1. Processing in background (non-blocking)
    2. Using cheaper LLM model (gpt-4o-mini instead of gpt-4)
    3. Batching memories efficiently
    4. Rate limiting to prevent API saturation

    Args:
        memory_ids: List of memory IDs to process
        tenant_id: Tenant UUID
        use_mini_model: Use cheaper model (gpt-4o-mini) for extraction
    """
    import asyncio
    import random

    async def main():
        # Rate limiting: Add initial delay to spread out workers and prevent herd behavior
        # This helps avoid hitting API rate limits when multiple tasks start simultaneously
        delay = random.uniform(0.5, 2.0)
        logger.info(
            "extract_graph_lazy_rate_limit_delay", delay=delay, tenant_id=tenant_id
        )
        await asyncio.sleep(delay)
        pool = await get_pool()
        try:
            # Initialize service with mini model if requested
            service = GraphExtractionService(pool)

            # Override LLM model if using mini model
            if use_mini_model and hasattr(service, "llm_provider"):
                service.llm_provider.model = "gpt-4o-mini"  # Cheaper model
                logger.info(
                    "using_mini_model_for_extraction",
                    model="gpt-4o-mini",
                    memory_count=len(memory_ids),
                )

            # Extract graph
            result = await service.extract_knowledge_graph(
                tenant_id=tenant_id,
                min_confidence=0.7,  # Higher threshold for background processing
                batch_size=50,
            )

            logger.info(
                "lazy_graph_extraction_complete",
                tenant_id=tenant_id,
                memory_count=len(memory_ids),
                triples_extracted=len(result.triples),
                entities_found=len(result.extracted_entities),
            )

            return {
                "success": True,
                "triples": len(result.triples),
                "entities": len(result.extracted_entities),
            }

        except Exception as e:
            logger.error(
                "lazy_graph_extraction_failed",
                tenant_id=tenant_id,
                error=str(e),
                memory_ids=memory_ids,
            )
            # Retry with exponential backoff
            raise self.retry(exc=e, countdown=60 * (2**self.request.retries))

        finally:
            await pool.close()

    return asyncio.run(main())


@celery_app.task
def process_graph_extraction_queue():
    """
    Periodically checks for memories waiting for graph extraction.

    Finds memories that:
    - Are episodic (layer='em')
    - Don't have graph data yet
    - Were created recently

    Then schedules them for lazy extraction.
    """
    import asyncio

    async def main():
        pool = await get_pool()
        try:
            # Find memories without graph extraction
            records = await pool.fetch(
                """
                SELECT DISTINCT tenant_id, ARRAY_AGG(id) as memory_ids
                FROM memories m
                WHERE layer = 'em'
                  AND created_at > NOW() - INTERVAL '1 hour'
                  AND NOT EXISTS (
                      SELECT 1 FROM graph_triples gt
                      WHERE gt.source_memory_id = m.id
                  )
                GROUP BY tenant_id
                LIMIT 100
            """
            )

            for record in records:
                tenant_id = record["tenant_id"]
                memory_ids = record["memory_ids"]

                # Schedule lazy extraction
                extract_graph_lazy.delay(
                    memory_ids=memory_ids, tenant_id=tenant_id, use_mini_model=True
                )

                logger.info(
                    "scheduled_lazy_extraction",
                    tenant_id=tenant_id,
                    memory_count=len(memory_ids),
                )

        finally:
            await pool.close()

    asyncio.run(main())


@celery_app.task
def run_entity_resolution_task(project_id: str = "default", tenant_id: str = "default"):
    """
    Periodic task for Pillar 1: Entity Resolution.
    Clusters and merges duplicate nodes.
    """
    import asyncio

    async def main():
        pool = await get_pool()
        try:
            service = EntityResolutionService(pool)
            await service.run_clustering_and_merging(project_id, tenant_id)
        finally:
            await pool.close()

    asyncio.run(main())


@celery_app.task
def run_community_detection_task(
    project_id: str = "default", tenant_id: str = "default"
):
    """
    Periodic task for Pillar 2: Community Detection & Summarization.
    Generates 'Wisdom' by summarizing clusters.
    """
    import asyncio

    async def main():
        pool = await get_pool()
        try:
            service = CommunityDetectionService(pool)
            await service.run_community_detection_and_summarization(
                project_id, tenant_id
            )
        finally:
            await pool.close()

    asyncio.run(main())


@celery_app.task(bind=True, max_retries=3)
def decay_memory_importance_task(self, tenant_id: str = None):
    """
    Enterprise-grade periodic task for memory importance decay.

    Applies temporal decay to memory importance scores across all tenants
    or a specific tenant. Uses ImportanceScoringService with sophisticated
    decay logic that considers:
    - Base decay rate for all memories
    - Accelerated decay for stale memories (not accessed > 30 days)
    - Protected decay for recently accessed memories (< 7 days)

    This task should be scheduled to run daily (e.g., at 2 AM) to maintain
    memory importance scores and naturally age memories over time.

    Args:
        tenant_id: Optional tenant ID to process. If None, processes all tenants.

    Returns:
        Dictionary with processing statistics
    """
    import asyncio
    from uuid import UUID

    from apps.memory_api.services.importance_scoring import ImportanceScoringService

    async def main():
        pool = await get_pool()
        try:
            # Initialize scoring service
            scoring_service = ImportanceScoringService(db=pool)

            # Get decay configuration from settings
            decay_rate = settings.MEMORY_DECAY_RATE
            logger.info(
                "decay_task_started",
                tenant_id=tenant_id,
                decay_rate=decay_rate,
            )

            total_updated = 0
            tenants_processed = 0
            failed_tenants = []

            if tenant_id:
                # Process single tenant
                try:
                    tenant_uuid = UUID(tenant_id)
                    updated = await scoring_service.decay_importance(
                        tenant_id=tenant_uuid,
                        decay_rate=decay_rate,
                        consider_access_stats=True,
                    )
                    total_updated += updated
                    tenants_processed = 1
                    logger.info(
                        "decay_tenant_complete",
                        tenant_id=tenant_id,
                        updated_count=updated,
                    )
                except Exception as e:
                    logger.error(
                        "decay_tenant_failed", tenant_id=tenant_id, error=str(e)
                    )
                    failed_tenants.append({"tenant_id": tenant_id, "error": str(e)})
            else:
                # Process all tenants
                # Get unique tenant IDs from memories table
                tenant_records = await pool.fetch(
                    """
                    SELECT DISTINCT tenant_id
                    FROM memories
                    WHERE importance > 0.01
                    """
                )

                logger.info(
                    "decay_processing_all_tenants",
                    tenant_count=len(tenant_records),
                    decay_rate=decay_rate,
                )

                for record in tenant_records:
                    try:
                        tenant_id_str = record["tenant_id"]
                        # Try to parse as UUID, if fails use as string
                        try:
                            tenant_uuid = UUID(tenant_id_str)
                        except (ValueError, AttributeError):
                            # If not a valid UUID, skip (could log warning)
                            logger.warning(
                                "invalid_tenant_id_format", tenant_id=tenant_id_str
                            )
                            continue

                        updated = await scoring_service.decay_importance(
                            tenant_id=tenant_uuid,
                            decay_rate=decay_rate,
                            consider_access_stats=True,
                        )
                        total_updated += updated
                        tenants_processed += 1

                        if updated > 0:
                            logger.info(
                                "decay_tenant_complete",
                                tenant_id=tenant_id_str,
                                updated_count=updated,
                            )
                    except Exception as e:
                        logger.error(
                            "decay_tenant_failed",
                            tenant_id=record["tenant_id"],
                            error=str(e),
                        )
                        failed_tenants.append(
                            {"tenant_id": record["tenant_id"], "error": str(e)}
                        )
                        # Continue processing other tenants

            result = {
                "success": True,
                "total_memories_updated": total_updated,
                "tenants_processed": tenants_processed,
                "failed_tenants": failed_tenants,
                "decay_rate": decay_rate,
            }

            logger.info(
                "decay_task_complete",
                total_updated=total_updated,
                tenants_processed=tenants_processed,
                failed_count=len(failed_tenants),
            )

            return result

        except Exception as e:
            logger.error("decay_task_fatal_error", error=str(e))
            # Retry with exponential backoff
            raise self.retry(exc=e, countdown=300 * (2**self.request.retries))

        finally:
            await pool.close()

    return asyncio.run(main())


# --- Celery Beat Schedule ---
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from celery.schedules import crontab

    # Schedule reflection checks every 5 minutes
    sender.add_periodic_task(
        300.0, schedule_reflections.s(), name="check for reflections every 5 mins"
    )
    # Schedule memory decay every hour (legacy, simple decay)
    sender.add_periodic_task(
        3600.0, apply_memory_decay.s(), name="apply memory decay every hour"
    )
    # Schedule importance decay daily at 2 AM (enterprise-grade decay)
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        decay_memory_importance_task.s(),
        name="decay memory importance daily at 2 AM",
    )
    # Schedule memory pruning once a day (86400 seconds)
    sender.add_periodic_task(
        86400.0, prune_old_memories.s(), name="prune old memories daily"
    )
    # Schedule graph extraction queue processing every 10 minutes
    sender.add_periodic_task(
        600.0,
        process_graph_extraction_queue.s(),
        name="process graph extraction queue every 10 mins",
    )
    # Schedule Entity Resolution every hour
    sender.add_periodic_task(
        3600.0, run_entity_resolution_task.s(), name="run entity resolution every hour"
    )
    # Schedule Community Detection every 6 hours
    sender.add_periodic_task(
        21600.0,
        run_community_detection_task.s(),
        name="run community detection every 6 hours",
    )
