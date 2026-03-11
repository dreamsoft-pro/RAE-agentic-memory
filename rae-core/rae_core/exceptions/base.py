"""
RAE Base Exceptions - Core Standard
"""

class RAEError(Exception):
    """Base exception for all RAE errors"""
    pass

class ContractViolationError(RAEError):
    """Raised when a Hard Frame 2.1 contract is violated"""
    pass

class InfrastructureError(RAEError):
    """Raised when infrastructure (Postgres, Qdrant, Ollama) fails"""
    pass

class SecurityPolicyViolationError(RAEError):
    """Raised when security boundaries are breached"""
    pass

class MemoryError(RAEError):
    """Raised when memory operations fail"""
    pass
