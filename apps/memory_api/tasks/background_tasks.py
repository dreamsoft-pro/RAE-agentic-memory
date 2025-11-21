from apps.memory_api.celery_app import celery_app
from apps.memory_api.services.reflection_engine import ReflectionEngine
from apps.memory_api.services.context_cache import rebuild_full_cache
from apps.memory_api.services.graph_extraction import GraphExtractionService
from apps.memory_api.config import settings
import asyncpg
import structlog

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
        records = await pool.fetch("""
            SELECT DISTINCT project, tenant_id
            FROM memories
            WHERE layer = 'em' AND created_at > NOW() - INTERVAL '1 hour'
        """)
        for record in records:
            generate_reflection_for_project.delay(record['project'], record['tenant_id'])
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
        await pool.execute("UPDATE memories SET strength = strength * $1", settings.MEMORY_DECAY_RATE)
        # Delete expired memories
        await pool.execute("DELETE FROM memories WHERE expires_at IS NOT NULL AND expires_at < NOW()")
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
            return # Pruning is disabled

        pool = await get_pool()
        try:
            interval = f"{settings.MEMORY_RETENTION_DAYS} days"
            # We only prune episodic memories, as semantic/reflective are meant to be long-term.
            result = await pool.execute(
                "DELETE FROM memories WHERE layer = 'em' AND created_at < NOW() - $1::interval",
                interval
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
def extract_graph_lazy(self, memory_ids: list, tenant_id: str, use_mini_model: bool = True):
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
        logger.info("extract_graph_lazy_rate_limit_delay", delay=delay, tenant_id=tenant_id)
        await asyncio.sleep(delay)
        pool = await get_pool()
        try:
            # Initialize service with mini model if requested
            service = GraphExtractionService(pool)

            # Override LLM model if using mini model
            if use_mini_model and hasattr(service, 'llm_provider'):
                original_model = service.llm_provider.model
                service.llm_provider.model = "gpt-4o-mini"  # Cheaper model
                logger.info(
                    "using_mini_model_for_extraction",
                    model="gpt-4o-mini",
                    memory_count=len(memory_ids)
                )

            # Extract graph
            result = await service.extract_knowledge_graph(
                tenant_id=tenant_id,
                min_confidence=0.7,  # Higher threshold for background processing
                batch_size=50
            )

            logger.info(
                "lazy_graph_extraction_complete",
                tenant_id=tenant_id,
                memory_count=len(memory_ids),
                triples_extracted=len(result.triples),
                entities_found=len(result.extracted_entities)
            )

            return {
                "success": True,
                "triples": len(result.triples),
                "entities": len(result.extracted_entities)
            }

        except Exception as e:
            logger.error(
                "lazy_graph_extraction_failed",
                tenant_id=tenant_id,
                error=str(e),
                memory_ids=memory_ids
            )
            # Retry with exponential backoff
            raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

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
            records = await pool.fetch("""
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
            """)

            for record in records:
                tenant_id = record['tenant_id']
                memory_ids = record['memory_ids']

                # Schedule lazy extraction
                extract_graph_lazy.delay(
                    memory_ids=memory_ids,
                    tenant_id=tenant_id,
                    use_mini_model=True
                )

                logger.info(
                    "scheduled_lazy_extraction",
                    tenant_id=tenant_id,
                    memory_count=len(memory_ids)
                )

        finally:
            await pool.close()

    asyncio.run(main())


# --- Celery Beat Schedule ---
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule reflection checks every 5 minutes
    sender.add_periodic_task(300.0, schedule_reflections.s(), name='check for reflections every 5 mins')
    # Schedule memory decay every hour
    sender.add_periodic_task(3600.0, apply_memory_decay.s(), name='apply memory decay every hour')
    # Schedule memory pruning once a day (86400 seconds)
    sender.add_periodic_task(86400.0, prune_old_memories.s(), name='prune old memories daily')
    # Schedule graph extraction queue processing every 10 minutes
    sender.add_periodic_task(600.0, process_graph_extraction_queue.s(), name='process graph extraction queue every 10 mins')
