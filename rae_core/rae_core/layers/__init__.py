"""
Memory layers for RAE-Core 4-layer architecture.

Layers:
- Sensory: Raw input buffer (milliseconds to seconds)
- Working: Active processing (seconds to minutes)
- LongTerm: Persistent storage (minutes to forever)
- Reflective: Meta-learning and insights (periodic synthesis)
"""

from rae_core.layers.base import BaseLayer
from rae_core.layers.longterm import LongTermMemoryLayer
from rae_core.layers.reflective import ReflectiveMemoryLayer
from rae_core.layers.sensory import SensoryLayer
from rae_core.layers.working import WorkingMemoryLayer

__all__ = [
    "BaseLayer",
    "SensoryLayer",
    "WorkingMemoryLayer",
    "LongTermMemoryLayer",
    "ReflectiveMemoryLayer",
]
