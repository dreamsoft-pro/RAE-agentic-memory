import logging
from typing import List

from redis.asyncio import Redis

from apps.memory_api.adapters.base import MemoryAdapter
from apps.memory_api.core.contract import (
    MemoryContract,
    ValidationResult,
    ValidationViolation,
)

logger = logging.getLogger(__name__)


class RedisAdapter(MemoryAdapter):
    """
    Validates Redis cache availability and compliance with the contract.
    """

    def __init__(self, client: Redis):
        self.client = client

    async def validate(self, contract: MemoryContract) -> ValidationResult:
        violations: List[ValidationViolation] = []

        if not contract.cache:
            # No cache requirements in contract
            return ValidationResult(valid=True, violations=[])

        try:
            # 1. Check connectivity
            if not await self.client.ping():
                violations.append(
                    ValidationViolation(
                        entity="redis",
                        issue_type="CONNECTION_FAILED",
                        details="Redis did not respond to PING.",
                    )
                )
                return ValidationResult(valid=False, violations=violations)

            # 2. Check namespaces (Logic: try to access/write to namespace)
            # Since Redis is schema-less, we mainly validate connectivity.
            # However, we can check if we have permissions (implicitly via write test).
            for namespace in contract.cache.required_namespaces:
                test_key = f"{namespace}validation_test_key"
                try:
                    await self.client.set(test_key, "1", ex=5)
                    val = await self.client.get(test_key)
                    if val != "1":
                        violations.append(
                            ValidationViolation(
                                entity="redis",
                                issue_type="WRITE_FAILED",
                                details=f"Could not verify write/read for namespace '{namespace}'.",
                            )
                        )
                except Exception as e:
                     violations.append(
                        ValidationViolation(
                            entity="redis",
                            issue_type="ACCESS_DENIED",
                            details=f"Error accessing namespace '{namespace}': {str(e)}",
                        )
                    )

        except Exception as e:
            logger.error(f"Redis validation failed: {e}")
            violations.append(
                ValidationViolation(
                    entity="redis",
                    issue_type="CONNECTION_ERROR",
                    details=str(e),
                )
            )

        return ValidationResult(valid=len(violations) == 0, violations=violations)
