"""
Memory Consolidation Service - Automatic memory layer transitions
"""

from typing import List, Dict, Optional, Any, Tuple
from uuid import UUID
from datetime import datetime, timedelta
from enum import Enum
import structlog

logger = structlog.get_logger(__name__)


class ConsolidationStrategy(str, Enum):
    """Strategies for memory consolidation"""
    PATTERN_BASED = "pattern_based"       # Look for recurring patterns
    IMPORTANCE_BASED = "importance_based" # Consolidate high-importance memories
    TIME_BASED = "time_based"             # Consolidate after time threshold
    SEMANTIC_CLUSTER = "semantic_cluster" # Group semantically similar memories
    MANUAL = "manual"                     # User-triggered consolidation


class ConsolidationResult:
    """Result of a consolidation operation"""

    def __init__(
        self,
        success: bool,
        source_memory_ids: List[str],
        target_memory_id: Optional[str] = None,
        target_layer: Optional[str] = None,
        consolidated_content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ):
        self.success = success
        self.source_memory_ids = source_memory_ids
        self.target_memory_id = target_memory_id
        self.target_layer = target_layer
        self.consolidated_content = consolidated_content
        self.metadata = metadata or {}
        self.error = error
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "source_memory_ids": self.source_memory_ids,
            "target_memory_id": self.target_memory_id,
            "target_layer": self.target_layer,
            "consolidated_content": self.consolidated_content,
            "metadata": self.metadata,
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }


class MemoryConsolidationService:
    """Service for automatic memory consolidation"""

    def __init__(
        self,
        db=None,
        vector_store=None,
        llm_client=None
    ):
        """
        Initialize memory consolidation service

        Args:
            db: Database connection
            vector_store: Vector store for similarity search
            llm_client: LLM client for content generation
        """
        self.db = db
        self.vector_store = vector_store
        self.llm_client = llm_client

    async def consolidate_episodic_to_working(
        self,
        tenant_id: UUID,
        max_memories: int = 100,
        min_importance: float = 0.5
    ) -> List[ConsolidationResult]:
        """
        Consolidate episodic memories to working memory

        Groups related episodic memories and creates working memory entries.

        Args:
            tenant_id: Tenant UUID
            max_memories: Maximum number of memories to process
            min_importance: Minimum importance score to consider

        Returns:
            List of consolidation results
        """
        logger.info(
            "consolidating_episodic_to_working",
            tenant_id=str(tenant_id),
            max_memories=max_memories,
            min_importance=min_importance
        )

        results = []

        # Get episodic memories ready for consolidation
        candidate_memories = await self._get_consolidation_candidates(
            tenant_id=tenant_id,
            source_layer="episodic",
            max_memories=max_memories,
            min_importance=min_importance
        )

        if not candidate_memories:
            logger.info("no_episodic_candidates_found")
            return results

        # Group memories by semantic similarity
        memory_groups = await self._group_similar_memories(candidate_memories)

        # Consolidate each group
        for group in memory_groups:
            result = await self._consolidate_group(
                tenant_id=tenant_id,
                memories=group,
                target_layer="working",
                strategy=ConsolidationStrategy.SEMANTIC_CLUSTER
            )
            results.append(result)

        logger.info(
            "episodic_consolidation_complete",
            total_groups=len(memory_groups),
            successful=sum(1 for r in results if r.success)
        )

        return results

    async def consolidate_working_to_semantic(
        self,
        tenant_id: UUID,
        max_memories: int = 50,
        min_age_days: int = 7
    ) -> List[ConsolidationResult]:
        """
        Consolidate working memories to semantic memory

        Extracts patterns and general knowledge from working memories.

        Args:
            tenant_id: Tenant UUID
            max_memories: Maximum number of memories to process
            min_age_days: Minimum age before consolidation

        Returns:
            List of consolidation results
        """
        logger.info(
            "consolidating_working_to_semantic",
            tenant_id=str(tenant_id),
            max_memories=max_memories,
            min_age_days=min_age_days
        )

        results = []

        # Get working memories ready for semantic consolidation
        cutoff_date = datetime.utcnow() - timedelta(days=min_age_days)

        candidate_memories = await self._get_consolidation_candidates(
            tenant_id=tenant_id,
            source_layer="working",
            max_memories=max_memories,
            created_before=cutoff_date
        )

        if not candidate_memories:
            logger.info("no_working_candidates_found")
            return results

        # Group by topic/pattern
        memory_groups = await self._group_by_patterns(candidate_memories)

        # Consolidate each group
        for group in memory_groups:
            result = await self._consolidate_group(
                tenant_id=tenant_id,
                memories=group,
                target_layer="semantic",
                strategy=ConsolidationStrategy.PATTERN_BASED
            )
            results.append(result)

        logger.info(
            "working_consolidation_complete",
            total_groups=len(memory_groups),
            successful=sum(1 for r in results if r.success)
        )

        return results

    async def consolidate_semantic_to_ltm(
        self,
        tenant_id: UUID,
        max_memories: int = 20,
        min_age_days: int = 30,
        min_importance: float = 0.7
    ) -> List[ConsolidationResult]:
        """
        Consolidate semantic memories to long-term memory (LTM)

        Only most important and stable knowledge moves to LTM.

        Args:
            tenant_id: Tenant UUID
            max_memories: Maximum number of memories to process
            min_age_days: Minimum age before LTM consolidation
            min_importance: Minimum importance score

        Returns:
            List of consolidation results
        """
        logger.info(
            "consolidating_semantic_to_ltm",
            tenant_id=str(tenant_id),
            max_memories=max_memories,
            min_age_days=min_age_days,
            min_importance=min_importance
        )

        results = []

        cutoff_date = datetime.utcnow() - timedelta(days=min_age_days)

        candidate_memories = await self._get_consolidation_candidates(
            tenant_id=tenant_id,
            source_layer="semantic",
            max_memories=max_memories,
            min_importance=min_importance,
            created_before=cutoff_date
        )

        if not candidate_memories:
            logger.info("no_semantic_candidates_found")
            return results

        # Each high-importance semantic memory becomes LTM
        for memory in candidate_memories:
            result = await self._consolidate_single(
                tenant_id=tenant_id,
                memory=memory,
                target_layer="ltm",
                strategy=ConsolidationStrategy.IMPORTANCE_BASED
            )
            results.append(result)

        logger.info(
            "semantic_consolidation_complete",
            total_processed=len(candidate_memories),
            successful=sum(1 for r in results if r.success)
        )

        return results

    async def _get_consolidation_candidates(
        self,
        tenant_id: UUID,
        source_layer: str,
        max_memories: int,
        min_importance: Optional[float] = None,
        created_before: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get memories eligible for consolidation

        Args:
            tenant_id: Tenant UUID
            source_layer: Source memory layer
            max_memories: Maximum to retrieve
            min_importance: Minimum importance filter
            created_before: Created before date filter

        Returns:
            List of memory dictionaries
        """
        # In production, query database with filters
        # For now, return empty list
        return []

    async def _group_similar_memories(
        self,
        memories: List[Dict[str, Any]],
        similarity_threshold: float = 0.7
    ) -> List[List[Dict[str, Any]]]:
        """
        Group memories by semantic similarity

        Args:
            memories: List of memory dictionaries
            similarity_threshold: Minimum similarity for grouping

        Returns:
            List of memory groups
        """
        if not memories:
            return []

        groups = []

        # In production:
        # 1. Calculate embeddings for all memories
        # 2. Use clustering (e.g., DBSCAN, hierarchical)
        # 3. Group similar memories together

        # For now, return each memory as its own group
        groups = [[memory] for memory in memories]

        return groups

    async def _group_by_patterns(
        self,
        memories: List[Dict[str, Any]]
    ) -> List[List[Dict[str, Any]]]:
        """
        Group memories by detected patterns

        Uses LLM to identify thematic patterns.

        Args:
            memories: List of memory dictionaries

        Returns:
            List of memory groups
        """
        if not memories:
            return []

        # In production:
        # 1. Use LLM to extract topics/themes
        # 2. Group by similar topics
        # 3. Consider temporal patterns

        # For now, return each memory as its own group
        return [[memory] for memory in memories]

    async def _consolidate_group(
        self,
        tenant_id: UUID,
        memories: List[Dict[str, Any]],
        target_layer: str,
        strategy: ConsolidationStrategy
    ) -> ConsolidationResult:
        """
        Consolidate a group of memories

        Args:
            tenant_id: Tenant UUID
            memories: List of memories to consolidate
            target_layer: Target memory layer
            strategy: Consolidation strategy

        Returns:
            ConsolidationResult
        """
        if not memories:
            return ConsolidationResult(
                success=False,
                source_memory_ids=[],
                error="No memories to consolidate"
            )

        source_ids = [m["id"] for m in memories]

        logger.info(
            "consolidating_memory_group",
            num_memories=len(memories),
            target_layer=target_layer,
            strategy=strategy.value
        )

        try:
            # Generate consolidated content using LLM
            consolidated_content = await self._generate_consolidated_content(
                memories=memories,
                target_layer=target_layer,
                strategy=strategy
            )

            # Create new memory in target layer
            target_memory_id = await self._create_consolidated_memory(
                tenant_id=tenant_id,
                content=consolidated_content,
                layer=target_layer,
                source_memory_ids=source_ids,
                strategy=strategy
            )

            # Mark source memories as consolidated
            await self._mark_as_consolidated(source_ids)

            return ConsolidationResult(
                success=True,
                source_memory_ids=source_ids,
                target_memory_id=target_memory_id,
                target_layer=target_layer,
                consolidated_content=consolidated_content,
                metadata={
                    "strategy": strategy.value,
                    "num_source_memories": len(memories)
                }
            )

        except Exception as e:
            logger.error(
                "consolidation_failed",
                error=str(e),
                num_memories=len(memories)
            )
            return ConsolidationResult(
                success=False,
                source_memory_ids=source_ids,
                error=str(e)
            )

    async def _consolidate_single(
        self,
        tenant_id: UUID,
        memory: Dict[str, Any],
        target_layer: str,
        strategy: ConsolidationStrategy
    ) -> ConsolidationResult:
        """
        Consolidate a single memory to target layer

        Args:
            tenant_id: Tenant UUID
            memory: Memory to consolidate
            target_layer: Target layer
            strategy: Consolidation strategy

        Returns:
            ConsolidationResult
        """
        return await self._consolidate_group(
            tenant_id=tenant_id,
            memories=[memory],
            target_layer=target_layer,
            strategy=strategy
        )

    async def _generate_consolidated_content(
        self,
        memories: List[Dict[str, Any]],
        target_layer: str,
        strategy: ConsolidationStrategy
    ) -> str:
        """
        Generate consolidated content using LLM

        Args:
            memories: Source memories
            target_layer: Target layer
            strategy: Consolidation strategy

        Returns:
            Consolidated content string
        """
        if not self.llm_client:
            # Fallback: simple concatenation
            return "\n\n".join(m.get("content", "") for m in memories)

        # Prepare prompt based on target layer and strategy
        prompt = self._build_consolidation_prompt(
            memories=memories,
            target_layer=target_layer,
            strategy=strategy
        )

        # Call LLM
        # In production: response = await self.llm_client.generate(prompt)
        # For now, return placeholder
        consolidated = f"Consolidated content from {len(memories)} memories"

        return consolidated

    def _build_consolidation_prompt(
        self,
        memories: List[Dict[str, Any]],
        target_layer: str,
        strategy: ConsolidationStrategy
    ) -> str:
        """Build LLM prompt for consolidation"""

        memory_contents = "\n\n".join([
            f"Memory {i+1}:\n{m.get('content', '')}"
            for i, m in enumerate(memories)
        ])

        if target_layer == "working":
            instruction = (
                "Consolidate these episodic memories into a coherent working memory. "
                "Focus on the main theme or task, preserving key details."
            )
        elif target_layer == "semantic":
            instruction = (
                "Extract the general knowledge and patterns from these working memories. "
                "Create a semantic memory that captures the core concepts, "
                "removing specific temporal details."
            )
        elif target_layer == "ltm":
            instruction = (
                "Refine this semantic knowledge into long-term memory format. "
                "Focus on timeless principles, patterns, and key facts. "
                "This should be stable, foundational knowledge."
            )
        else:
            instruction = "Consolidate these memories into a summary."

        prompt = f"""{instruction}

Source Memories:
{memory_contents}

Consolidated Memory:"""

        return prompt

    async def _create_consolidated_memory(
        self,
        tenant_id: UUID,
        content: str,
        layer: str,
        source_memory_ids: List[str],
        strategy: ConsolidationStrategy
    ) -> str:
        """
        Create a new consolidated memory

        Args:
            tenant_id: Tenant UUID
            content: Consolidated content
            layer: Target layer
            source_memory_ids: IDs of source memories
            strategy: Consolidation strategy

        Returns:
            New memory ID
        """
        # In production, create memory in database
        # For now, return mock ID
        import uuid
        new_memory_id = str(uuid.uuid4())

        logger.info(
            "consolidated_memory_created",
            memory_id=new_memory_id,
            layer=layer,
            num_sources=len(source_memory_ids)
        )

        return new_memory_id

    async def _mark_as_consolidated(self, memory_ids: List[str]):
        """
        Mark source memories as consolidated

        Args:
            memory_ids: List of memory IDs to mark
        """
        # In production, update memories in database
        # Set is_consolidated=True, consolidation_timestamp=now
        pass

    async def run_automatic_consolidation(
        self,
        tenant_id: UUID
    ) -> Dict[str, Any]:
        """
        Run full automatic consolidation pipeline

        Consolidates memories through all layers:
        Episodic -> Working -> Semantic -> LTM

        Args:
            tenant_id: Tenant UUID

        Returns:
            Summary of consolidation results
        """
        logger.info(
            "starting_automatic_consolidation",
            tenant_id=str(tenant_id)
        )

        summary = {
            "tenant_id": str(tenant_id),
            "started_at": datetime.utcnow().isoformat(),
            "episodic_to_working": [],
            "working_to_semantic": [],
            "semantic_to_ltm": [],
            "total_consolidated": 0,
            "errors": []
        }

        try:
            # Phase 1: Episodic -> Working
            episodic_results = await self.consolidate_episodic_to_working(tenant_id)
            summary["episodic_to_working"] = [r.to_dict() for r in episodic_results]

            # Phase 2: Working -> Semantic
            working_results = await self.consolidate_working_to_semantic(tenant_id)
            summary["working_to_semantic"] = [r.to_dict() for r in working_results]

            # Phase 3: Semantic -> LTM
            semantic_results = await self.consolidate_semantic_to_ltm(tenant_id)
            summary["semantic_to_ltm"] = [r.to_dict() for r in semantic_results]

            # Calculate totals
            all_results = episodic_results + working_results + semantic_results
            summary["total_consolidated"] = sum(1 for r in all_results if r.success)

            # Collect errors
            summary["errors"] = [
                {"source_ids": r.source_memory_ids, "error": r.error}
                for r in all_results
                if not r.success and r.error
            ]

        except Exception as e:
            logger.error("automatic_consolidation_failed", error=str(e))
            summary["errors"].append({"error": str(e)})

        summary["completed_at"] = datetime.utcnow().isoformat()

        logger.info(
            "automatic_consolidation_complete",
            tenant_id=str(tenant_id),
            total_consolidated=summary["total_consolidated"]
        )

        return summary

    async def get_consolidation_stats(
        self,
        tenant_id: UUID,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Get consolidation statistics

        Args:
            tenant_id: Tenant UUID
            period_days: Period to analyze

        Returns:
            Statistics dictionary
        """
        # In production, query actual consolidation history
        return {
            "tenant_id": str(tenant_id),
            "period_days": period_days,
            "total_consolidations": 0,
            "by_layer": {
                "episodic_to_working": 0,
                "working_to_semantic": 0,
                "semantic_to_ltm": 0
            },
            "by_strategy": {
                strategy.value: 0
                for strategy in ConsolidationStrategy
            },
            "avg_memories_per_consolidation": 0.0,
            "success_rate": 1.0
        }

    async def revert_consolidation(
        self,
        consolidated_memory_id: str
    ) -> bool:
        """
        Revert a consolidation operation

        Restores source memories and removes consolidated memory.

        Args:
            consolidated_memory_id: ID of consolidated memory

        Returns:
            Success status
        """
        logger.info(
            "reverting_consolidation",
            memory_id=consolidated_memory_id
        )

        try:
            # In production:
            # 1. Find source memory IDs
            # 2. Mark source memories as not consolidated
            # 3. Delete or archive consolidated memory

            logger.info(
                "consolidation_reverted",
                memory_id=consolidated_memory_id
            )
            return True

        except Exception as e:
            logger.error(
                "revert_failed",
                memory_id=consolidated_memory_id,
                error=str(e)
            )
            return False

    async def preview_consolidation(
        self,
        tenant_id: UUID,
        memory_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Preview what consolidation would produce

        Args:
            tenant_id: Tenant UUID
            memory_ids: IDs of memories to consolidate

        Returns:
            Preview with consolidated content
        """
        # Fetch memories
        memories = []  # In production, fetch from DB

        # Generate preview content
        preview_content = await self._generate_consolidated_content(
            memories=memories,
            target_layer="semantic",  # Default preview layer
            strategy=ConsolidationStrategy.SEMANTIC_CLUSTER
        )

        return {
            "source_memory_ids": memory_ids,
            "num_memories": len(memory_ids),
            "preview_content": preview_content,
            "estimated_layer": "semantic"
        }
