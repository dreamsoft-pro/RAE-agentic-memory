"""
ReflectionEngineV2 - Actor-Evaluator-Reflector Pattern Implementation

This service implements the RAE v1 Reflective Memory system following
the Actor → Evaluator → Reflector pattern described in the implementation plan.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from uuid import UUID

import asyncpg
import structlog

from apps.memory_api.config import settings
from apps.memory_api.models.reflection_v2_models import (
    LLMReflectionResponse,  # Added import for LLMReflectionResponse
)
from apps.memory_api.models.reflection_v2_models import (
    Event,
    OutcomeType,
    ReflectionContext,
    ReflectionResult,
)
from apps.memory_api.services.llm import get_llm_provider

if TYPE_CHECKING:
    from apps.memory_api.services.rae_core_service import RAECoreService

logger = structlog.get_logger(__name__)


# ... (rest of imports and prompts)


# ============================================================================
# ReflectionEngineV2
# ============================================================================


class ReflectionEngineV2:
    """
    Enhanced Reflection Engine implementing Actor-Evaluator-Reflector pattern.

    This engine generates reflections from:
    - Failures (errors, timeouts, validation failures)
    - Successes (valuable strategies, patterns)
    - Partial outcomes (incomplete but informative)

    Features:
    - Structured reflection generation using LLM
    - Importance and confidence scoring
    - Automatic categorization and tagging
    - Storage to memory_items with proper typing
    - Graph linking in Qdrant (optional)
    """

    def __init__(
        self,
        pool: asyncpg.Pool,
        rae_service: "RAECoreService",
    ):
        """
        Initialize ReflectionEngineV2

        Args:
            pool: Database connection pool
            rae_service: RAECoreService for memory operations
        """
        self.pool = pool
        self.rae_service = rae_service
        self.llm_provider = get_llm_provider()

    # ... (generate_reflection, _generate_failure_reflection, _generate_success_reflection, _format_events methods remain same)

    async def store_reflection(
        self,
        result: ReflectionResult,
        tenant_id: str,
        project_id: str,
        session_id: Optional[UUID] = None,
    ) -> Dict[str, str]:
        """
        Store reflection result to database.

        Stores both reflection and strategy (if present) as separate memory items
        with proper memory_type classification.

        Args:
            result: ReflectionResult to store
            tenant_id: Tenant identifier
            project_id: Project identifier
            session_id: Optional session identifier

        Returns:
            Dict with reflection_id and optional strategy_id
        """
        stored_ids = {}

        # Store reflection
        reflection_id = await self.rae_service.store_memory(
            tenant_id=tenant_id,
            project=project_id,
            content=result.reflection_text,
            source="reflection_engine_v2",
            importance=result.importance,
            layer="reflective",  # Reflective Memory layer
            tags=result.tags,
        )

        stored_ids["reflection_id"] = reflection_id

        logger.info(
            "reflection_stored",
            tenant_id=tenant_id,
            project_id=project_id,
            reflection_id=reflection_id,
            importance=result.importance,
        )

        # Store strategy if present
        if result.strategy_text:
            strategy_id = await self.rae_service.store_memory(
                tenant_id=tenant_id,
                project=project_id,
                content=result.strategy_text,
                source="reflection_engine_v2",
                importance=result.importance * 1.1,  # Strategies slightly more important
                layer="reflective",
                tags=result.tags + ["strategy"],
            )

            stored_ids["strategy_id"] = strategy_id

            logger.info(
                "strategy_stored",
                tenant_id=tenant_id,
                project_id=project_id,
                strategy_id=strategy_id,
            )

        return stored_ids

    async def query_reflections(
        self,
        tenant_id: str,
        project_id: str,
        query_text: Optional[str] = None,
        k: int = 5,
        min_importance: float = 0.5,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query reflections from memory.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            query_text: Optional semantic query
            k: Number of results
            min_importance: Minimum importance threshold
            tags: Optional tag filters

        Returns:
            List of reflection records
        """
        # For now, use basic repository query
        # In production, this would use vector search + filtering
        reflections = await self.rae_service.list_memories(
            tenant_id=tenant_id, 
            layer="reflective",
            project=project_id,
            limit=100
        )

        # Simple filtering by importance
        filtered = [r for r in reflections if r.get("importance", 0) >= min_importance]

        # Limit results
        return filtered[:k]
