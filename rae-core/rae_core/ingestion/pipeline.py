"""
RAE Universal Ingest Pipeline (UICTC).
Orchestrator for deterministic and auditable ingestion.
"""

from typing import Any, Dict, List, Optional
import structlog
from .interfaces import IngestChunk, ContentSignature
from .normalizer import IngestNormalizer
from .detector import ContentSignatureDetector
from .policy import IngestPolicySelector
from .segmenter import IngestSegmenter
from .compressor import IngestCompressor

logger = structlog.get_logger(__name__)

class UniversalIngestPipeline:
    """
    Orchestrates the 5-stage ingestion process.
    Ensures every memory block has a signature and audit trail.
    """
    
    def __init__(self):
        self.normalizer = IngestNormalizer()
        self.detector = ContentSignatureDetector()
        self.policy_selector = IngestPolicySelector()
        self.segmenter = IngestSegmenter()
        self.compressor = IngestCompressor()
        
    async def process(self, raw_text: str, metadata: Optional[Dict[str, Any]] = None) -> tuple[List[IngestChunk], ContentSignature, List[Dict[str, Any]]]:
        """
        Runs the full pipeline.
        Returns: (chunks, signature, audit_trail)
        """
        audit_trail = []
        
        # 1. Normalize
        normalized_text, audit_norm = self.normalizer.normalize(raw_text, metadata)
        audit_trail.append(audit_norm.__dict__)
        
        # 2. Detect Signature
        signature, audit_det = self.detector.detect(normalized_text)
        audit_trail.append(audit_det.__dict__)
        
        # 3. Select Policy
        policy, audit_pol = self.policy_selector.select_policy(signature)
        audit_trail.append(audit_pol.__dict__)
        
        # 4. Segment
        chunks, audit_seg = self.segmenter.segment(normalized_text, policy, signature)
        audit_trail.append(audit_seg.__dict__)
        
        # 5. Compress
        compressed_chunks, prov_map, audit_comp = self.compressor.compress(chunks, policy)
        audit_trail.append(audit_comp.__dict__)
        
        # 6. Attach provenance to chunks
        for i, chunk in enumerate(compressed_chunks):
            chunk.metadata.update({
                "ingest_signature": signature.to_dict(),
                "ingest_policy": policy,
                "ingest_version": "1.0.0",
                "compression_provenance": prov_map.get(i, [i])
            })
            
        logger.info("universal_ingest_complete", 
                    policy=policy, 
                    chunk_count=len(compressed_chunks), 
                    mode=signature.struct.get("mode"))
                    
        return compressed_chunks, signature, audit_trail
