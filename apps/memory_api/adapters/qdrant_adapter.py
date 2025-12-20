import logging
from typing import List

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance

from apps.memory_api.adapters.base import MemoryAdapter
from apps.memory_api.core.contract import (
    MemoryContract,
    ValidationResult,
    ValidationViolation,
)

logger = logging.getLogger(__name__)


class QdrantAdapter(MemoryAdapter):
    """
    Validates Qdrant vector store compliance with the contract.
    """

    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def validate(self, contract: MemoryContract) -> ValidationResult:
        violations: List[ValidationViolation] = []

        if not contract.vector_store:
            return ValidationResult(valid=True, violations=[])

        try:
            # Get existing collections
            collections_resp = await self.client.get_collections()
            existing_collections = {c.name for c in collections_resp.collections}

            for col_contract in contract.vector_store.collections:
                if col_contract.name not in existing_collections:
                    violations.append(
                        ValidationViolation(
                            entity=col_contract.name,
                            issue_type="MISSING_COLLECTION",
                            details=f"Qdrant collection '{col_contract.name}' is missing.",
                        )
                    )
                    continue

                # Inspect collection config
                col_info = await self.client.get_collection(col_contract.name)
                
                # Check vector size (assuming named vector 'dense' or default un-named)
                # RAE usually uses named vectors, let's check config.
                config = col_info.config.params.vectors
                
                # Qdrant config can be a single VectorParams or dict of VectorParams
                actual_size = None
                actual_distance = None

                # Handle different vector configs (single vs multi-vector)
                # Assuming 'dense' vector for RAE based on qdrant_store.py
                if isinstance(config, dict) and "dense" in config:
                    actual_size = config["dense"].size
                    actual_distance = config["dense"].distance
                elif hasattr(config, "size"): # Single vector
                     actual_size = config.size
                     actual_distance = config.distance
                else:
                     # Fallback or error
                     violations.append(
                        ValidationViolation(
                            entity=col_contract.name,
                            issue_type="CONFIG_ERROR",
                            details=f"Could not determine vector config for '{col_contract.name}'.",
                        )
                    )
                     continue

                if actual_size != col_contract.vector_size:
                    violations.append(
                        ValidationViolation(
                            entity=col_contract.name,
                            issue_type="DIMENSION_MISMATCH",
                            details=f"Collection '{col_contract.name}' has dimension {actual_size}, expected {col_contract.vector_size}.",
                        )
                    )

                # Normalize distance metric check (simple string compare)
                # Qdrant enums: Distance.COSINE, Distance.EUCLID, etc.
                # Contract string: "Cosine"
                # We can map contract string to Qdrant enum or just log warning if strict.
                # For now let's be lenient or skip distance check if complexity is high, 
                # but let's try basic check.
                expected_dist = col_contract.distance_metric.lower() # cosine
                actual_dist_str = str(actual_distance).lower().replace("distance.", "") # cosine
                
                if expected_dist != actual_dist_str:
                     violations.append(
                        ValidationViolation(
                            entity=col_contract.name,
                            issue_type="METRIC_MISMATCH",
                            details=f"Collection '{col_contract.name}' uses {actual_dist_str}, expected {expected_dist}.",
                        )
                    )


        except Exception as e:
            logger.error(f"Qdrant validation failed: {e}")
            violations.append(
                ValidationViolation(
                    entity="qdrant",
                    issue_type="CONNECTION_ERROR",
                    details=str(e),
                )
            )

        return ValidationResult(valid=len(violations) == 0, violations=violations)
