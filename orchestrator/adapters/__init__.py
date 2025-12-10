"""Adapters for different AI model CLIs/APIs."""

from .base import (
    ModelAdapter,
    ModelType,
    TaskComplexity,
    TaskRisk,
    AgentContext,
    AgentResult,
)
from .claude_adapter import ClaudeAdapter
from .gemini_adapter import GeminiAdapter

__all__ = [
    "ModelAdapter",
    "ModelType",
    "TaskComplexity",
    "TaskRisk",
    "AgentContext",
    "AgentResult",
    "ClaudeAdapter",
    "GeminiAdapter",
]
