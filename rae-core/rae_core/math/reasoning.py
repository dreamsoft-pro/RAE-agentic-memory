"""Reasoning controller for graph reasoning with configurable parameters.

Centralizes control of reasoning depth, uncertainty handling, and path pruning.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

logger = logging.getLogger(__name__)


@dataclass
class ReasoningPath:
    """Represents a reasoning chain/path through the knowledge graph.

    A path consists of:
    - nodes: Sequence of node IDs visited
    - steps: Human-readable step descriptions
    - uncertainty: Confidence score (0-1, higher is better)
    - contradictions: Any detected contradictions
    - metadata: Additional path information
    """

    nodes: List[UUID] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    uncertainty: float = 1.0  # Start with full confidence
    contradictions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tokens_used: int = 0

    @property
    def depth(self) -> int:
        """Current depth of reasoning path."""
        return len(self.steps)

    @property
    def is_contradictory(self) -> bool:
        """Check if path has contradictions."""
        return len(self.contradictions) > 0

    def add_step(
        self,
        node_id: UUID,
        description: str,
        uncertainty_delta: float = 0.0,
        tokens: int = 0,
    ):
        """Add a reasoning step to the path.

        Args:
            node_id: Node ID being visited
            description: Human-readable step description
            uncertainty_delta: Change in uncertainty (-1 to +1)
            tokens: Tokens consumed by this step
        """
        self.nodes.append(node_id)
        self.steps.append(description)
        self.uncertainty = max(0.0, min(1.0, self.uncertainty + uncertainty_delta))
        self.tokens_used += tokens

    def aligns_with(self, memory: Dict[str, Any]) -> bool:
        """Check if path aligns with a memory.

        Args:
            memory: Memory dictionary with content and metadata

        Returns:
            True if path content is consistent with memory
        """
        # Simple heuristic: check if memory content appears in any step
        memory_content = memory.get("content", "").lower()
        if not memory_content:
            return False

        # Check if any step mentions similar content
        for step in self.steps:
            if memory_content in step.lower():
                return True

        return False


class ReasoningController:
    """Centralized controller for graph reasoning with configurable parameters.

    Features:
    - Configurable max depth, uncertainty threshold, token budget
    - Decision logic for continuing vs stopping reasoning
    - Path pruning based on contradictions and memory alignment
    - Statistics tracking for debugging

    Usage:
        controller = ReasoningController(
            max_depth=12,
            uncertainty_threshold=0.3,
            token_budget_per_step=500,
        )

        # During reasoning
        if controller.should_continue_reasoning(
            current_depth=path.depth,
            uncertainty=path.uncertainty,
            tokens_used=path.tokens_used,
        ):
            # Continue reasoning
            pass
        else:
            # Stop reasoning
            pass
    """

    def __init__(
        self,
        max_depth: int = 12,
        uncertainty_threshold: float = 0.3,
        token_budget_per_step: int = 500,
        enable_pruning: bool = True,
    ):
        """Initialize reasoning controller.

        Args:
            max_depth: Maximum reasoning depth before stopping
            uncertainty_threshold: Stop if uncertainty drops below this
            token_budget_per_step: Maximum tokens per reasoning step
            enable_pruning: Enable automatic path pruning
        """
        self.max_depth = max_depth
        self.uncertainty_threshold = uncertainty_threshold
        self.token_budget = token_budget_per_step
        self.enable_pruning = enable_pruning

        # Statistics
        self.stats = {
            "paths_evaluated": 0,
            "paths_pruned": 0,
            "max_depth_reached": 0,
            "uncertainty_stops": 0,
            "budget_exceeded": 0,
        }

    def should_continue_reasoning(
        self,
        current_depth: int,
        uncertainty: float,
        tokens_used: int,
    ) -> bool:
        """Decide whether to continue or stop reasoning.

        Args:
            current_depth: Current depth of reasoning path
            uncertainty: Current uncertainty score (0-1)
            tokens_used: Tokens consumed so far

        Returns:
            True if should continue, False if should stop
        """
        self.stats["paths_evaluated"] += 1

        # Check max depth
        if current_depth >= self.max_depth:
            self.stats["max_depth_reached"] += 1
            logger.debug(f"Stopping: Max depth {self.max_depth} reached")
            return False

        # Check uncertainty (higher uncertainty = less confident)
        # If uncertainty drops below threshold, we're too uncertain to continue
        if uncertainty < self.uncertainty_threshold:
            self.stats["uncertainty_stops"] += 1
            logger.debug(
                f"Stopping: Uncertainty {uncertainty:.2f} below threshold "
                f"{self.uncertainty_threshold}"
            )
            return False

        # Check token budget
        if tokens_used > self.token_budget:
            self.stats["budget_exceeded"] += 1
            logger.debug(
                f"Stopping: Tokens {tokens_used} exceed budget {self.token_budget}"
            )
            return False

        return True

    def prune_contradictory_paths(
        self,
        paths: List[ReasoningPath],
        episodic_memories: Optional[List[Dict[str, Any]]] = None,
        semantic_memories: Optional[List[Dict[str, Any]]] = None,
    ) -> List[ReasoningPath]:
        """Cut paths that contradict memory layers.

        Args:
            paths: List of reasoning paths to evaluate
            episodic_memories: Recent episodic memories for validation
            semantic_memories: Semantic knowledge for validation

        Returns:
            Filtered list of non-contradictory paths
        """
        if not self.enable_pruning:
            return paths

        pruned_paths = []

        for path in paths:
            # Skip paths with detected contradictions
            if path.is_contradictory:
                self.stats["paths_pruned"] += 1
                logger.debug(
                    f"Pruning path (depth {path.depth}): Has contradictions"
                )
                continue

            # Check alignment with episodic memory
            if episodic_memories:
                contradicts_episodic = self._contradicts_memories(
                    path, episodic_memories
                )
                if contradicts_episodic:
                    self.stats["paths_pruned"] += 1
                    logger.debug(
                        f"Pruning path (depth {path.depth}): "
                        "Contradicts episodic memory"
                    )
                    continue

            # Check alignment with semantic memory
            if semantic_memories:
                contradicts_semantic = self._contradicts_memories(
                    path, semantic_memories
                )
                if contradicts_semantic:
                    self.stats["paths_pruned"] += 1
                    logger.debug(
                        f"Pruning path (depth {path.depth}): "
                        "Contradicts semantic knowledge"
                    )
                    continue

            # Path passes all checks
            pruned_paths.append(path)

        return pruned_paths

    def _contradicts_memories(
        self, path: ReasoningPath, memories: List[Dict[str, Any]]
    ) -> bool:
        """Check if path contradicts any memories.

        Simple heuristic: If path doesn't align with any memory,
        it might be contradictory.

        Args:
            path: Reasoning path to check
            memories: Memories to validate against

        Returns:
            True if path contradicts memories
        """
        if not memories:
            return False

        # Check if path aligns with at least one memory
        aligns_with_any = any(path.aligns_with(mem) for mem in memories)

        # If path doesn't align with any memory, consider it contradictory
        return not aligns_with_any

    def get_stats(self) -> Dict[str, int]:
        """Get reasoning statistics.

        Returns:
            Dictionary with reasoning stats
        """
        return self.stats.copy()

    def reset_stats(self):
        """Reset statistics counters."""
        for key in self.stats:
            self.stats[key] = 0
