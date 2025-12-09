"""
Context builder for synthesizing memory context.

Builds coherent context from multiple memories for LLM consumption.
"""

from typing import Any, Dict, List, Optional

from rae_core.models.memory import ScoredMemoryRecord


class ContextBuilder:
    """
    Context builder for synthesizing memory context.

    Takes retrieved memories and builds a coherent context string
    suitable for LLM prompts or agent reasoning.
    """

    def __init__(
        self,
        max_context_length: int = 4000,
        include_metadata: bool = True,
        format_style: str = "markdown"
    ):
        """
        Initialize context builder.

        Args:
            max_context_length: Maximum context length in characters
            include_metadata: Whether to include memory metadata
            format_style: Output format ("markdown", "json", "plain")
        """
        self.max_context_length = max_context_length
        self.include_metadata = include_metadata
        self.format_style = format_style

    async def build_context(
        self,
        memories: List[ScoredMemoryRecord],
        query: Optional[str] = None,
        template: Optional[str] = None
    ) -> str:
        """
        Build context from memories.

        Args:
            memories: List of scored memories
            query: Optional query that triggered retrieval
            template: Optional custom template

        Returns:
            Formatted context string
        """
        if not memories:
            return "No relevant memories found."

        if self.format_style == "markdown":
            return self._build_markdown_context(memories, query)
        elif self.format_style == "json":
            return self._build_json_context(memories, query)
        else:
            return self._build_plain_context(memories, query)

    def _build_markdown_context(
        self,
        memories: List[ScoredMemoryRecord],
        query: Optional[str]
    ) -> str:
        """Build markdown-formatted context."""
        lines = []

        if query:
            lines.append(f"# Context for: {query}\n")

        lines.append(f"## Retrieved Memories ({len(memories)} results)\n")

        current_length = len('\n'.join(lines))

        for i, memory in enumerate(memories, 1):
            # Build memory block
            memory_block = f"### Memory {i} (Score: {memory.score:.3f})\n\n"

            if self.include_metadata:
                memory_block += f"- **Layer**: {memory.layer}\n"
                memory_block += f"- **Importance**: {memory.importance:.2f}\n"
                memory_block += f"- **Timestamp**: {memory.timestamp}\n"
                if memory.tags:
                    memory_block += f"- **Tags**: {', '.join(memory.tags)}\n"
                memory_block += "\n"

            memory_block += f"**Content**:\n{memory.content}\n\n"
            memory_block += "---\n\n"

            # Check if adding this memory would exceed max length
            if current_length + len(memory_block) > self.max_context_length:
                lines.append(f"_(Truncated - {len(memories) - i + 1} memories omitted)_\n")
                break

            lines.append(memory_block)
            current_length += len(memory_block)

        return ''.join(lines)

    def _build_json_context(
        self,
        memories: List[ScoredMemoryRecord],
        query: Optional[str]
    ) -> str:
        """Build JSON-formatted context."""
        import json

        context = {
            "query": query,
            "memory_count": len(memories),
            "memories": []
        }

        current_length = len(json.dumps(context))

        for memory in memories:
            memory_dict = {
                "id": memory.id,
                "content": memory.content,
                "score": memory.score,
                "layer": memory.layer,
                "importance": memory.importance
            }

            if self.include_metadata:
                memory_dict["timestamp"] = memory.timestamp.isoformat()
                memory_dict["tags"] = memory.tags
                memory_dict["usage_count"] = memory.usage_count

            memory_json = json.dumps(memory_dict)

            if current_length + len(memory_json) > self.max_context_length:
                break

            context["memories"].append(memory_dict)
            current_length += len(memory_json)

        return json.dumps(context, indent=2)

    def _build_plain_context(
        self,
        memories: List[ScoredMemoryRecord],
        query: Optional[str]
    ) -> str:
        """Build plain text context."""
        lines = []

        if query:
            lines.append(f"Query: {query}\n")

        lines.append(f"Retrieved {len(memories)} memories:\n\n")

        current_length = len('\n'.join(lines))

        for i, memory in enumerate(memories, 1):
            memory_text = f"[{i}] {memory.content}\n"

            if self.include_metadata:
                memory_text += f"    (Score: {memory.score:.3f}, Importance: {memory.importance:.2f})\n"

            memory_text += "\n"

            if current_length + len(memory_text) > self.max_context_length:
                lines.append(f"(Truncated - {len(memories) - i + 1} memories omitted)\n")
                break

            lines.append(memory_text)
            current_length += len(memory_text)

        return ''.join(lines)

    async def build_layered_context(
        self,
        memories_by_layer: Dict[str, List[ScoredMemoryRecord]],
        query: Optional[str] = None
    ) -> str:
        """
        Build context organized by layer.

        Args:
            memories_by_layer: Memories grouped by layer
            query: Optional query

        Returns:
            Formatted context with layer separation
        """
        lines = []

        if query:
            lines.append(f"# Context for: {query}\n\n")

        # Order: reflective → longterm → working → sensory
        layer_order = ["reflective", "longterm", "working", "sensory"]

        for layer_name in layer_order:
            memories = memories_by_layer.get(layer_name, [])
            if not memories:
                continue

            lines.append(f"## {layer_name.capitalize()} Layer ({len(memories)} memories)\n\n")

            for i, memory in enumerate(memories, 1):
                memory_block = f"**{i}.** {memory.content}\n"
                if self.include_metadata:
                    memory_block += f"   _(Score: {memory.score:.3f}, Importance: {memory.importance:.2f})_\n"
                memory_block += "\n"

                lines.append(memory_block)

            lines.append("\n")

        return ''.join(lines)
