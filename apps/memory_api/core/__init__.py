"""
RAE Core - Mathematical formalization of RAE system.

This module contains the core mathematical abstractions:
  - State: s_t  S (state space)
  - Actions: a_t  A (action space)
  - Transitions: P(s_{t+1} | s_t, a_t)
  - Rewards: R(s_t, a_t, s_{t+1})

These abstractions enable:
  1. MDP formulation for optimal control
  2. Information bottleneck for context selection
  3. Graph update operators for knowledge evolution
"""

from apps.memory_api.core.state import (
    BudgetState,
    GraphState,
    MemoryLayerState,
    MemoryState,
    RAEState,
    WorkingContext,
)

__all__ = [
    "RAEState",
    "WorkingContext",
    "MemoryState",
    "MemoryLayerState",
    "BudgetState",
    "GraphState",
]
