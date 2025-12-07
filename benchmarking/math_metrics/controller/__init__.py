"""
Math Layer Controller

Central controller for deciding which mathematical level (L1, L2, L3) to use
for memory operations in RAE.

Main exports:
    MathLayerController: Main controller class
    MathDecision: Standardized decision format
    TaskContext: Input context for decisions
    MathLevel: Enum for math levels
    TaskType: Enum for task types
    Features: Feature extraction dataclass

Usage:
    from benchmarking.math_metrics.controller import (
        MathLayerController,
        TaskContext,
        TaskType,
    )

    controller = MathLayerController()
    context = TaskContext(task_type=TaskType.MEMORY_RETRIEVE)
    decision = controller.decide(context)
"""

from .controller import MathLayerController, FeatureExtractor
from .decision import MathDecision, DecisionWithOutcome
from .context import TaskContext
from .features import Features
from .types import MathLevel, TaskType
from .config import MathControllerConfig, LoggingConfig, SafetyConfig, load_config
from .integration import (
    MathControllerIntegration,
    get_math_controller,
    set_math_controller,
)

__all__ = [
    # Main classes
    "MathLayerController",
    "FeatureExtractor",

    # Data structures
    "MathDecision",
    "DecisionWithOutcome",
    "TaskContext",
    "Features",

    # Enums
    "MathLevel",
    "TaskType",

    # Configuration
    "MathControllerConfig",
    "LoggingConfig",
    "SafetyConfig",
    "load_config",

    # Integration helpers
    "MathControllerIntegration",
    "get_math_controller",
    "set_math_controller",
]
