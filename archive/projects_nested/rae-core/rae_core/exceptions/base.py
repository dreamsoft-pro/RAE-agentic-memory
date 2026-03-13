from typing import Any, Dict, Optional

class RAEError(Exception):
    """Base class for all RAE exceptions."""
    def __init__(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.metadata = metadata or {}

class InfrastructureError(RAEError):
    """Raised when a component like Postgres or Qdrant fails."""
    pass

class ContractViolationError(RAEError):
    """Raised when an agent output violates Hard Frames 2.0."""
    pass

class EpistemicConflictError(RAEError):
    """Raised when a severe contradiction is found between memory layers."""
    pass

class MathStabilityError(RAEError):
    """Raised when weights or resonance factors become unstable."""
    pass

class SecurityPolicyViolationError(RAEError):
    """Raised when ISO 27000/42001 policies are breached."""
    pass

class ResourceDriftError(RAEError):
    """Raised by OCP when a managed resource deviates from desired state."""
    pass
