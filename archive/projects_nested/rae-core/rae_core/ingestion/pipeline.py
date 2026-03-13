from typing import Any, Dict, List, Optional
import structlog
import yaml
import os
import hashlib

from .interfaces import IngestChunk, ContentSignature, IngestAudit
from .normalizer import IngestNormalizer
from .detector import ContentSignatureDetector
from .policy import IngestPolicySelector
from .segmenter import IngestSegmenter
from .compressor import IngestCompressor

logger = structlog.get_logger(__name__)

class IngestContractViolation(Exception):
    """Raised when a specific ingestion stage violates global contracts."""
    pass

class UniversalIngestPipeline:
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.normalizer = IngestNormalizer()
        self.detector = ContentSignatureDetector()
        self.policy_selector = IngestPolicySelector()
        self.segmenter = IngestSegmenter(config=self.config)
        self.compressor = IngestCompressor()

    def _load_config(self, path: Optional[str]) -> Dict[str, Any]:
        paths = ["config/math_controller.yaml", "/app/math_config/math_controller.yaml", "../config/math_controller.yaml"]
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f: return yaml.safe_load(f) or {}
                except: continue
        return {}

    async def process(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> tuple[List[IngestChunk], ContentSignature, List[IngestAudit], str]:
        audit_trail = []
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Stage 1: Normalize
        normalized_text, audit_1 = self.normalizer.normalize(text, metadata)
        audit_trail.append(audit_1)
        
        # Stage 2: Detect Signature + Contract Gate
        signature, audit_2 = self.detector.detect(normalized_text)
        if signature.dist.get("token_entropy", 0) < 1.0:
            logger.warning("ingest_contract_warning", stage="signature", reason="low_entropy")
        audit_trail.append(audit_2)
        
        # Stage 3: Policy Selection + Contract Gate
        policy, audit_3 = self.policy_selector.select_policy(signature)
        if metadata and metadata.get("info_class") == "restricted" and policy != "POLICY_SECURE":
            logger.error("ingest_contract_violation", stage="policy", reason="security_mismatch")
            # Enforce hard contract
            policy = "POLICY_SECURE" 
        audit_trail.append(audit_3)
        
        # Stage 4: Segmentation
        chunks, audit_4 = self.segmenter.segment(normalized_text, policy, signature)
        audit_trail.append(audit_4)
        
        for chunk in chunks:
            if not chunk.metadata: chunk.metadata = {}
            chunk.metadata["content_hash"] = text_hash

        # Stage 5: Compression
        compressed_chunks, prov_map, audit_5 = self.compressor.compress(chunks, policy)
        audit_trail.append(audit_5)
        
        for i, chunk in enumerate(compressed_chunks):
            if not chunk.metadata: chunk.metadata = {}
            chunk.metadata.update({
                "ingest_signature": signature.to_dict(),
                "ingest_policy": policy,
                "ingest_version": "1.1.0", # Incremented for Contract Awareness
                "compression_provenance": prov_map.get(i, [i]),
                "contract_verified": True
            })
            
        logger.info("universal_ingest_complete", chunk_count=len(compressed_chunks), policy=policy)
        return compressed_chunks, signature, audit_trail, policy
