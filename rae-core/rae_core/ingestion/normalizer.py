"""
RAE Ingest Normalizer.
Stage 1 of the Universal Ingest Pipeline.
"""

from typing import Any, Dict, Optional
from .interfaces import INormalizer, IngestAudit

class IngestNormalizer(INormalizer):
    """
    Standardizes input text for analysis.
    Performs cleaning and metadata attachment.
    """
    
    def normalize(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> tuple[str, IngestAudit]:
        original_len = len(text)
        
        # 1. Basic Cleaning (preserving newlines for structure)
        # Remove null bytes
        normalized = text.replace('\x00', '')
        
        # Normalize line endings to LF
        normalized = normalized.replace('\r\n', '\n').replace('\r', '\n')
        
        # 2. Trace
        audit = IngestAudit(
            stage="normalize",
            action="standardize_text",
            trace={
                "original_length": original_len,
                "normalized_length": len(normalized),
                "source_metadata": metadata or {}
            }
        )
        
        return normalized, audit
