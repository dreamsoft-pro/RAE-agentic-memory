"""
RAE Universal Segmenter (Stage 4).
Policy-driven chunking.
"""

import re
from typing import Any, Dict, List
from .interfaces import ISegmenter, ContentSignature, IngestChunk, IngestAudit

class IngestSegmenter(ISegmenter):
    """
    Splits text into chunks according to the selected policy.
    """
    
    def segment(self, text: str, policy: str, signature: ContentSignature) -> tuple[List[IngestChunk], IngestAudit]:
        chunks = []
        
        if policy == "POLICY_LOG_STREAM":
            chunks = self._segment_logs(text)
        elif policy == "POLICY_PROCEDURE_DOC":
            chunks = self._segment_procedural(text)
        elif policy == "POLICY_MIXED_SAFE":
            chunks = self._segment_mixed(text)
        else:
            # Default prose-like chunking
            chunks = self._segment_default(text)
            
        audit = IngestAudit(
            stage="segment",
            action="text_splitting",
            trace={
                "policy": policy,
                "chunk_count": len(chunks)
            }
        )
        
        return chunks, audit

    def _segment_logs(self, text: str, lines_per_chunk: int = 50) -> List[IngestChunk]:
        lines = text.split('\n')
        chunks = []
        offset = 0
        for i in range(0, len(lines), lines_per_chunk):
            chunk_lines = lines[i:i + lines_per_chunk]
            content = '\n'.join(chunk_lines)
            chunks.append(IngestChunk(
                content=content,
                metadata={"log_sequence": i // lines_per_chunk},
                offset=offset,
                length=len(content)
            ))
            offset += len(content) + 1 # +1 for the stripped newline
        return chunks

    def _segment_procedural(self, text: str, max_size: int = 1500) -> List[IngestChunk]:
        # Split by steps or double newlines
        parts = re.split(r'(\n\s*(?:Step|Krok|Kolejno)\s*\d+[:.]|\n\n)', text)
        
        chunks = []
        current_chunk = ""
        current_offset = 0
        chunk_offset = 0
        
        for part in parts:
            if not part: continue
            if len(current_chunk) + len(part) < max_size:
                current_chunk += part
            else:
                if current_chunk:
                    chunks.append(IngestChunk(
                        content=current_chunk.strip(),
                        metadata={"type": "procedural_step"},
                        offset=chunk_offset,
                        length=len(current_chunk)
                    ))
                chunk_offset += len(current_chunk)
                current_chunk = part
                
        if current_chunk:
            chunks.append(IngestChunk(
                content=current_chunk.strip(),
                metadata={"type": "procedural_step"},
                offset=chunk_offset,
                length=len(current_chunk)
            ))
            
        return chunks

    def _segment_default(self, text: str, chunk_size: int = 1000) -> List[IngestChunk]:
        # Paragraph based chunking
        paras = text.split('\n\n')
        chunks = []
        current_chunk = ""
        offset = 0
        chunk_offset = 0
        
        for para in paras:
            if not para: continue
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(IngestChunk(
                        content=current_chunk.strip(),
                        metadata={},
                        offset=chunk_offset,
                        length=len(current_chunk)
                    ))
                chunk_offset += len(current_chunk)
                current_chunk = para + "\n\n"
                
        if current_chunk:
            chunks.append(IngestChunk(
                content=current_chunk.strip(),
                metadata={},
                offset=chunk_offset,
                length=len(current_chunk)
            ))
        return chunks

    def _segment_mixed(self, text: str) -> List[IngestChunk]:
        # Fallback to a tighter paragraph split
        return self._segment_default(text, chunk_size=800)
