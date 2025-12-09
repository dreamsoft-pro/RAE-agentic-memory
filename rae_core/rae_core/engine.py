"""
RAE Engine - Main entry point for RAE-Core.

The RAE Engine orchestrates all components:
- 4-layer memory architecture
- Hybrid search
- Reflection generation
- Context building
"""

from typing import Any, Dict, List, Optional

from rae_core.context.builder import ContextBuilder
from rae_core.layers import (
    LongTermMemoryLayer,
    ReflectiveMemoryLayer,
    SensoryLayer,
    WorkingMemoryLayer,
)
from rae_core.models.memory import MemoryRecord, QueryMemoryResponse, ScoredMemoryRecord
from rae_core.reflection.engine import ReflectionEngine
from rae_core.scoring.scorer import ImportanceScorer
from rae_core.search.engine import SearchEngine


class RAEEngine:
    """
    RAE Engine - Main orchestrator for memory operations.

    This is the primary interface for interacting with RAE-Core.
    It manages all four memory layers and provides high-level operations.
    """

    def __init__(
        self,
        sensory_max_size: int = 100,
        sensory_retention_seconds: int = 10,
        working_max_size: int = 50,
        working_retention_minutes: int = 30,
        enable_auto_consolidation: bool = True,
        enable_reflections: bool = True
    ):
        """
        Initialize RAE Engine.

        Args:
            sensory_max_size: Max size of sensory layer
            sensory_retention_seconds: Sensory layer retention time
            working_max_size: Max size of working memory
            working_retention_minutes: Working memory retention time
            enable_auto_consolidation: Auto-consolidate between layers
            enable_reflections: Auto-generate reflections
        """
        # Initialize layers
        self.sensory = SensoryLayer(
            max_size=sensory_max_size,
            retention_seconds=sensory_retention_seconds
        )
        self.working = WorkingMemoryLayer(
            max_size=working_max_size,
            retention_minutes=working_retention_minutes
        )
        self.longterm = LongTermMemoryLayer()
        self.reflective = ReflectiveMemoryLayer()

        # Initialize components
        self.search_engine = SearchEngine()
        self.reflection_engine = ReflectionEngine()
        self.context_builder = ContextBuilder()
        self.importance_scorer = ImportanceScorer()

        # Configuration
        self.enable_auto_consolidation = enable_auto_consolidation
        self.enable_reflections = enable_reflections

    async def store_memory(
        self,
        content: str,
        source: Optional[str] = None,
        importance: Optional[float] = None,
        layer: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None
    ) -> str:
        """
        Store a new memory in appropriate layer.

        Args:
            content: Memory content
            source: Memory source
            importance: Initial importance (calculated if not provided)
            layer: Target layer (auto-determined if not provided)
            tags: Optional tags
            tenant_id: Tenant ID for multi-tenancy
            project: Project identifier

        Returns:
            Memory ID
        """
        from datetime import datetime
        from uuid import uuid4

        # Calculate importance if not provided
        if importance is None:
            importance = 0.5  # Default

        # Create memory record
        memory = MemoryRecord(
            id=f"mem_{uuid4().hex[:12]}",
            tenant_id=tenant_id,
            content=content,
            source=source,
            importance=importance,
            layer=layer or "stm",
            tags=tags,
            timestamp=datetime.now(),
            project=project
        )

        # Determine target layer
        if not layer:
            # Start in sensory for new input
            target_layer = self.sensory
        elif layer == "sensory" or layer == "stm":
            target_layer = self.sensory
        elif layer == "working":
            target_layer = self.working
        elif layer == "longterm" or layer == "ltm":
            target_layer = self.longterm
        elif layer == "reflective" or layer == "rm":
            target_layer = self.reflective
        else:
            target_layer = self.longterm  # Default

        # Store memory
        memory_id = await target_layer.store(memory)

        # Auto-consolidation
        if self.enable_auto_consolidation:
            await self._auto_consolidate()

        return memory_id

    async def query_memory(
        self,
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        search_layers: Optional[List[str]] = None
    ) -> QueryMemoryResponse:
        """
        Query memories across layers.

        Args:
            query: Query text
            k: Number of results
            filters: Optional filters
            search_layers: Layers to search (default: all)

        Returns:
            Query response with scored memories
        """
        # Determine layers to search
        if not search_layers:
            layers = [self.reflective, self.longterm, self.working, self.sensory]
        else:
            layer_map = {
                "reflective": self.reflective,
                "longterm": self.longterm,
                "working": self.working,
                "sensory": self.sensory
            }
            layers = [layer_map[name] for name in search_layers if name in layer_map]

        # Execute multi-layer search
        results = await self.search_engine.search_multi_layer(
            layers=layers,
            query=query,
            k=k,
            filters=filters
        )

        # Build context
        context = await self.context_builder.build_context(results, query)

        # Get statistics
        stats = {
            "total_results": len(results),
            "layers_searched": [layer.name for layer in layers]
        }

        return QueryMemoryResponse(
            results=results,
            synthesized_context=context,
            graph_statistics=stats
        )

    async def consolidate_memories(
        self,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Manually trigger memory consolidation across layers.

        Returns:
            Dictionary of consolidated memory IDs by transition
        """
        results = {}

        # Sensory → Working
        sensory_to_working = await self.sensory.consolidate(
            self.working,
            criteria={"importance_threshold": 0.5}
        )
        results["sensory_to_working"] = sensory_to_working

        # Working → Long-term
        working_to_longterm = await self.working.consolidate(
            self.longterm,
            criteria={
                "importance_threshold": 0.6,
                "min_usage": 2,
                "min_age_minutes": 10
            }
        )
        results["working_to_longterm"] = working_to_longterm

        # Long-term → Reflective (via reflection engine)
        if self.enable_reflections:
            reflections = await self.reflection_engine.generate_reflections(
                source_layer=self.longterm,
                target_layer=self.reflective,
                tenant_id=tenant_id,
                project=project
            )
            results["longterm_to_reflective"] = [r.id for r in reflections]

        return results

    async def generate_reflections(
        self,
        tenant_id: Optional[str] = None,
        project: Optional[str] = None
    ) -> List[MemoryRecord]:
        """
        Generate reflections from long-term memories.

        Args:
            tenant_id: Optional tenant filter
            project: Optional project filter

        Returns:
            List of generated reflections
        """
        reflections = await self.reflection_engine.generate_reflections(
            source_layer=self.longterm,
            target_layer=self.reflective,
            tenant_id=tenant_id,
            project=project
        )

        return reflections

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics across all layers.

        Returns:
            Statistics dictionary
        """
        stats = {
            "sensory": await self.sensory.get_statistics(),
            "working": await self.working.get_statistics(),
            "longterm": await self.longterm.get_statistics(),
            "reflective": await self.reflective.get_statistics(),
            "total_memories": (
                (await self.sensory.get_statistics())["count"] +
                (await self.working.get_statistics())["count"] +
                (await self.longterm.get_statistics())["count"] +
                (await self.reflective.get_statistics())["count"]
            )
        }

        return stats

    async def clear_all(self, tenant_id: Optional[str] = None) -> Dict[str, int]:
        """
        Clear all memories across all layers.

        Args:
            tenant_id: Optional tenant filter

        Returns:
            Count of cleared memories per layer
        """
        return {
            "sensory": await self.sensory.clear(tenant_id),
            "working": await self.working.clear(tenant_id),
            "longterm": await self.longterm.clear(tenant_id),
            "reflective": await self.reflective.clear(tenant_id)
        }

    async def _auto_consolidate(self):
        """Auto-consolidation triggered after each store."""
        # Simple consolidation: promote high-importance from sensory to working
        await self.sensory.consolidate(
            self.working,
            criteria={"importance_threshold": 0.6}
        )
