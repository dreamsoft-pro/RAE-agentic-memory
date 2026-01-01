"""Base exceptions for RAE-core."""

class RAEError(Exception):
    """Base exception for all RAE-core errors."""
    pass

class StorageError(RAEError):
    """Exception raised for errors in storage adapters."""
    pass

class ValidationError(RAEError):
    """Exception raised for validation failures."""
    pass
