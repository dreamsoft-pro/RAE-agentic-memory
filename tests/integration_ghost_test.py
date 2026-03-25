import asyncio
import uuid
import asyncpg
import json
import structlog
from apps.memory_api.services.rae_core_service import RAECoreService
from rae_core.config.settings import RAESettings
from apps.memory_api.models.reflection_models import ReflectionType, ReflectionScoring

logger = structlog.get_logger()

async def test_reflection_db_persistence():
    settings = RAESettings()
    dsn = "postgresql://rae:rae_password@rae-postgres:5432/rae"
    pool = await asyncpg.create_pool(dsn)
    
    try:
        rae = RAECoreService(postgres_pool=pool)
        tenant_id = str(uuid.uuid4())
        project = "ghostbusters-final-test"
        
        print(f"👻 Starting Persistence Test for Tenant: {tenant_id}")
        
        # 1. Zapisujemy wspomnienie przez serwis
        mem_id = await rae.store_memory(
            tenant_id=tenant_id,
            project=project,
            content="Ghostbusters check: Testing functional repository pattern.",
            source="test_agent",
            layer="episodic"
        )
        print(f"✅ Stored in memories: {mem_id}")
        
        # 2. Test zapisu przez repository (funkcja create_reflection)
        from apps.memory_api.repositories.reflection_repository import create_reflection
        
        scoring = ReflectionScoring(
            novelty_score=0.9,
            importance_score=0.8,
            utility_score=0.7,
            confidence_score=1.0
        )
        
        # POPRAWKA: Serializacja metadata do JSON String dla asyncpg
        refl_unit = await create_reflection(
            pool=pool,
            tenant_id=tenant_id,
            project=project,
            content="Functional reflection test successful.",
            reflection_type=ReflectionType.ANALYSIS,
            priority=3,
            scoring=scoring,
            metadata=json.dumps({"test": "value"}) # asyncpg JSONB needs string usually
        )
        print(f"✅ Stored in 'reflections' table: {refl_unit.id}")
        
        # 3. Weryfikacja
        count = await pool.fetchval("SELECT count(*) FROM reflections WHERE id = $1", refl_unit.id)
        if count > 0:
            print("🔥 SUCCESS: All ghosts are gone. Reflection DB persistence is 100% functional.")

    finally:
        await pool.close()

if __name__ == "__main__":
    asyncio.run(test_reflection_db_persistence())
