"""Context builder for assembling LLM-ready context from search results."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID

from rae_core.context.window import ContextWindowManager, estimate_tokens
from rae_core.models.context import ContextMetadata, WorkingContext


class ContextFormat(str, Enum):
    """Format types for context assembly."""

    CONVERSATIONAL = "conversational"
    STRUCTURED = "structured"
    MINIMAL = "minimal"
    DETAILED = "detailed"


class ContextBuilder:
    """
    Builds LLM-ready context from memory search results.

    Features:
    - Token-aware context assembly
    - Priority-based memory ranking
    - Multiple formatting templates
    - Automatic truncation on overflow
    - Metadata preservation
    """

    def __init__(
        self,
        max_tokens: int = 4096,
        default_format: ContextFormat = ContextFormat.CONVERSATIONAL,
    ):
        """Initialize context builder.

        Args:
            max_tokens: Maximum tokens for assembled context
            default_format: Default context format template
        """
        self.max_tokens = max_tokens
        self.default_format = default_format
        self.window_manager = ContextWindowManager(max_tokens=max_tokens)

    def build_context(
        self,
        memories: list[dict[str, Any]],
        query: str | None = None,
        format_type: ContextFormat | None = None,
        max_memories: int | None = None,
        include_metadata: bool = True,
    ) -> tuple[str, ContextMetadata]:
        """Build context from search results.

        Args:
            memories: List of memory records from search
            query: Optional query that produced these results
            format_type: Context format (uses default if not specified)
            max_memories: Maximum number of memories to include
            include_metadata: Include memory metadata in context

        Returns:
            Tuple of (formatted_context, context_metadata)
        """
        format_type = format_type or self.default_format

        # Rank memories by priority
        ranked_memories = self._rank_memories(memories)

        # Apply max_memories limit if specified
        if max_memories:
            ranked_memories = ranked_memories[:max_memories]

        # Build context with token management
        context_parts = []
        included_memories = []
        total_tokens = 0

        # Add query header if provided
        if query:
            query_header = self._format_query_header(query, format_type)
            query_tokens = estimate_tokens(query_header)
            if query_tokens <= self.max_tokens:
                context_parts.append(query_header)
                total_tokens += query_tokens

        # Add memories until token limit
        for memory in ranked_memories:
            memory_text = self._format_memory(
                memory, format_type, include_metadata=include_metadata
            )
            memory_tokens = estimate_tokens(memory_text)

            # Check if adding this memory would exceed limit
            if total_tokens + memory_tokens > self.max_tokens:
                break

            context_parts.append(memory_text)
            included_memories.append(memory)
            total_tokens += memory_tokens

            # Update window manager
            memory_id = memory.get("id")
            if memory_id and isinstance(memory_id, (str, UUID)):
                if isinstance(memory_id, str):
                    memory_id = UUID(memory_id)
                self.window_manager.add_item(memory_id, memory_tokens)

        # Assemble final context
        context = self._assemble_context(context_parts, format_type)

        # Build metadata
        metadata = ContextMetadata(
            total_items=len(memories),
            active_items=len(included_memories),
            token_usage=total_tokens,
            last_compaction=(
                datetime.now(timezone.utc)
                if len(included_memories) < len(memories)
                else None
            ),
            statistics={
                "format": format_type,
                "truncated": len(included_memories) < len(memories),
                "query_provided": query is not None,
                "avg_tokens_per_memory": (
                    total_tokens // len(included_memories) if included_memories else 0
                ),
            },
        )

        return context, metadata

    def build_working_context(
        self,
        tenant_id: str,
        agent_id: str | None,
        memories: list[dict[str, Any]],
        focus_items: list[UUID] | None = None,
    ) -> WorkingContext:
        """Build WorkingContext model from memories.

        Args:
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            memories: List of memory records
            focus_items: Optional list of high-priority memory IDs

        Returns:
            WorkingContext model
        """
        # Create context window
        window = self.window_manager.create_window()

        # Add memories to window
        for memory in memories:
            memory_id = memory.get("id")
            if memory_id and isinstance(memory_id, (str, UUID)):
                if isinstance(memory_id, str):
                    memory_id = UUID(memory_id)
                memory_text = memory.get("content", "")
                tokens = estimate_tokens(str(memory_text))
                self.window_manager.add_item(memory_id, tokens)

        # Calculate priority score
        priority_score = self._calculate_priority_score(memories, focus_items or [])

        return WorkingContext(
            tenant_id=tenant_id,
            agent_id=agent_id,
            window=window,
            focus_items=focus_items or [],
            priority_score=priority_score,
            metadata={
                "memory_count": len(memories),
                "focus_count": len(focus_items or []),
            },
        )

    def _rank_memories(self, memories: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Rank memories by priority (importance, recency, relevance).

        Args:
            memories: List of memory records

        Returns:
            Sorted list of memories (highest priority first)
        """

        def priority_score(memory: dict[str, Any]) -> float:
            # Base score from importance
            importance = memory.get("importance", 0.5)

            # Bonus for recency (up to +0.2)
            modified_at = memory.get("modified_at")
            recency_bonus = 0.0
            if modified_at:
                if isinstance(modified_at, str):
                    try:
                        modified_at = datetime.fromisoformat(
                            modified_at.replace("Z", "+00:00")
                        )
                    except Exception:
                        modified_at = None

                if isinstance(modified_at, datetime):
                    # Ensure modified_at is timezone-aware (assume UTC if naive)
                    if modified_at.tzinfo is None:
                        modified_at = modified_at.replace(tzinfo=timezone.utc)

                    age_hours = (
                        datetime.now(timezone.utc) - modified_at
                    ).total_seconds() / 3600
                    # More recent = higher bonus
                    recency_bonus = 0.2 * (1.0 / (1.0 + age_hours / 24))

            # Bonus for relevance score (from search)
            relevance = memory.get("score", 0.0)
            relevance_bonus = 0.3 * relevance

            return float(importance + recency_bonus + relevance_bonus)

        return sorted(memories, key=priority_score, reverse=True)

    def _format_query_header(self, query: str, format_type: ContextFormat) -> str:
        """Format query header based on format type.

        Args:
            query: Query string
            format_type: Context format

        Returns:
            Formatted query header
        """
        if format_type == ContextFormat.MINIMAL:
            return f"Query: {query}\n"
        elif format_type == ContextFormat.STRUCTURED:
            return f"# Query\n{query}\n\n# Relevant Memories\n"
        elif format_type == ContextFormat.DETAILED:
            return f"## Search Query\n{query}\n\n## Retrieved Memories (ranked by relevance)\n"
        else:  # CONVERSATIONAL
            return (
                f"Based on your query: '{query}'\n\nHere are the relevant memories:\n\n"
            )

    def _format_memory(
        self,
        memory: dict[str, Any],
        format_type: ContextFormat,
        include_metadata: bool = True,
    ) -> str:
        """Format single memory based on format type.

        Args:
            memory: Memory record
            format_type: Context format
            include_metadata: Include metadata fields

        Returns:
            Formatted memory string
        """
        content = memory.get("content", "")
        memory_id = memory.get("id", "unknown")
        importance = memory.get("importance", 0.0)
        tags = memory.get("tags", [])
        created_at = memory.get("created_at")

        if format_type == ContextFormat.MINIMAL:
            return f"{content}\n"

        elif format_type == ContextFormat.STRUCTURED:
            parts = [f"## Memory {memory_id}", f"{content}"]
            if include_metadata:
                parts.append(f"Importance: {importance:.2f}")
                if tags:
                    parts.append(f"Tags: {', '.join(tags)}")
            return "\n".join(parts) + "\n\n"

        elif format_type == ContextFormat.DETAILED:
            parts = [
                f"### Memory: {memory_id}",
                f"**Content:** {content}",
            ]
            if include_metadata:
                parts.append(f"**Importance:** {importance:.2f}")
                if tags:
                    parts.append(f"**Tags:** {', '.join(tags)}")
                if created_at:
                    parts.append(f"**Created:** {created_at}")
            return "\n".join(parts) + "\n\n"

        else:  # CONVERSATIONAL
            if include_metadata and importance > 0.7:
                return f"- {content} [Important]\n"
            return f"- {content}\n"

    def _assemble_context(self, parts: list[str], format_type: ContextFormat) -> str:
        """Assemble context parts into final string.

        Args:
            parts: List of context parts
            format_type: Context format

        Returns:
            Assembled context string
        """
        if format_type == ContextFormat.MINIMAL:
            return "".join(parts)
        elif format_type in [ContextFormat.STRUCTURED, ContextFormat.DETAILED]:
            return "\n".join(parts)
        else:  # CONVERSATIONAL
            return "\n".join(parts)

    def _calculate_priority_score(
        self, memories: list[dict[str, Any]], focus_items: list[UUID]
    ) -> float:
        """Calculate overall priority score for working context.

        Args:
            memories: List of memory records
            focus_items: High-priority memory IDs

        Returns:
            Priority score (0-1)
        """
        if not memories:
            return 0.0

        # Average importance of all memories
        avg_importance = sum(m.get("importance", 0.5) for m in memories) / len(memories)

        # Boost if focus items are present
        focus_boost = 0.2 if focus_items else 0.0

        # Token utilization factor
        utilization = self.window_manager.get_utilization()
        utilization_factor = 0.1 * utilization

        return float(min(1.0, avg_importance + focus_boost + utilization_factor))

    def reset(self) -> None:
        """Reset builder state and create new window."""
        self.window_manager.create_window()

    def get_statistics(self) -> dict[str, Any]:
        """Get builder statistics.

        Returns:
            Dictionary with builder statistics
        """
        return {
            "max_tokens": self.max_tokens,
            "default_format": self.default_format,
            "window_utilization": self.window_manager.get_utilization(),
            "window_tokens": (
                self.window_manager.current_window.current_tokens
                if self.window_manager.current_window
                else 0
            ),
        }
