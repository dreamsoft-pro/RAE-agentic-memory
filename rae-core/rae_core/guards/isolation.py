"""Memory isolation guard for preventing cross-agent/session leaks.

Post-search validation that results belong to correct agent/session.
This is a defensive layer that catches any leaks that slip through
the primary namespace guards in adapters.
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

logger = logging.getLogger(__name__)


class MemoryIsolationGuard:
    """Validates that memory search results match expected agent/session IDs.

    This is a defensive layer that provides post-search validation.
    Even if adapter-level namespace guards have bugs, this catches leaks.

    Usage:
        guard = MemoryIsolationGuard()
        validated_memories = guard.validate_search_results(
            results=raw_results,
            expected_agent_id="agent-123",
            expected_session_id="session-456"
        )
    """

    def __init__(self, strict_mode: bool = True):
        """Initialize isolation guard.

        Args:
            strict_mode: If True, log warnings for any detected leaks.
                        If False, silently filter leaks.
        """
        self.strict_mode = strict_mode
        self.leak_count = 0
        self.validation_count = 0

    def validate_search_results(
        self,
        results: List[Dict[str, Any]],
        expected_agent_id: str,
        expected_session_id: Optional[str] = None,
        expected_tenant_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Filter out any memories that don't match expected IDs.

        Args:
            results: Raw search results from adapter
            expected_agent_id: Expected agent ID
            expected_session_id: Expected session ID (optional)
            expected_tenant_id: Expected tenant ID (optional)

        Returns:
            Filtered list of memories that pass validation
        """
        self.validation_count += 1
        validated = []

        for memory in results:
            # Extract IDs from memory
            memory_agent_id = memory.get("agent_id")
            memory_session_id = memory.get("session_id")
            memory_tenant_id = memory.get("tenant_id")

            # Validate agent_id (mandatory)
            if memory_agent_id != expected_agent_id:
                self._log_leak(
                    "agent_id",
                    expected=expected_agent_id,
                    actual=memory_agent_id,
                    memory_id=memory.get("id"),
                )
                continue

            # Validate session_id if provided
            if expected_session_id and memory_session_id != expected_session_id:
                self._log_leak(
                    "session_id",
                    expected=expected_session_id,
                    actual=memory_session_id,
                    memory_id=memory.get("id"),
                )
                continue

            # Validate tenant_id if provided
            if expected_tenant_id and memory_tenant_id != expected_tenant_id:
                self._log_leak(
                    "tenant_id",
                    expected=expected_tenant_id,
                    actual=memory_tenant_id,
                    memory_id=memory.get("id"),
                )
                continue

            # All validations passed
            validated.append(memory)

        # Log summary if any leaks detected
        leaks_detected = len(results) - len(validated)
        if leaks_detected > 0:
            logger.warning(
                f"MemoryIsolationGuard: Filtered {leaks_detected}/{len(results)} "
                f"leaked memories (agent_id={expected_agent_id}, "
                f"session_id={expected_session_id})"
            )

        return validated

    def validate_single_memory(
        self,
        memory: Dict[str, Any],
        expected_agent_id: str,
        expected_session_id: Optional[str] = None,
        expected_tenant_id: Optional[str] = None,
    ) -> bool:
        """Validate a single memory.

        Args:
            memory: Memory dictionary
            expected_agent_id: Expected agent ID
            expected_session_id: Expected session ID (optional)
            expected_tenant_id: Expected tenant ID (optional)

        Returns:
            True if memory passes validation, False otherwise
        """
        results = self.validate_search_results(
            [memory], expected_agent_id, expected_session_id, expected_tenant_id
        )
        return len(results) > 0

    def _log_leak(
        self,
        field: str,
        expected: Any,
        actual: Any,
        memory_id: Optional[UUID] = None,
    ):
        """Log a detected memory leak."""
        self.leak_count += 1

        if self.strict_mode:
            logger.warning(
                f"MEMORY LEAK DETECTED: Wrong {field} - "
                f"expected '{expected}', got '{actual}' "
                f"(memory_id={memory_id})"
            )

    def get_stats(self) -> Dict[str, int]:
        """Get isolation guard statistics.

        Returns:
            Dictionary with leak_count and validation_count
        """
        return {
            "leak_count": self.leak_count,
            "validation_count": self.validation_count,
            "leak_rate": (
                self.leak_count / self.validation_count if self.validation_count > 0 else 0
            ),
        }

    def reset_stats(self):
        """Reset leak and validation counters."""
        self.leak_count = 0
        self.validation_count = 0
