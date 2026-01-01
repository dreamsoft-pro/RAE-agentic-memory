"""Memory isolation guard for RAE-core.

Provides post-search validation to ensure data isolation between agents and sessions.
"""

import logging
from typing import Any, List

from ..models.memory import Memory

logger = logging.getLogger(__name__)


class MemoryIsolationGuard:
    """
    Guards against multi-layer memory interference (MMIT).

    Validates that search results belong to the correct agent and session
    before returning them to the caller.
    """

    def validate_search_results(
        self,
        results: List[Memory],
        expected_agent_id: str,
        expected_session_id: str,
        raise_on_leak: bool = False,
    ) -> List[Memory]:
        """
        Filter out any memories that don't match expected IDs.

        Args:
            results: List of memories retrieved from storage
            expected_agent_id: The ID of the agent performing the search
            expected_session_id: The current session ID
            raise_on_leak: Whether to raise an exception if a leak is detected

        Returns:
            Filtered list of memories belonging only to the expected agent/session
        """
        validated = []
        leaks_detected = 0

        for memory in results:
            agent_id = getattr(memory, "agent_id", None)
            session_id = getattr(memory, "session_id", None)

            # Check agent_id match
            if agent_id != expected_agent_id:
                logger.warning(
                    f"MMIT LEAK DETECTED: Memory {memory.id} has wrong agent_id "
                    f"({agent_id} != expected {expected_agent_id})"
                )
                leaks_detected += 1
                continue

            # Check session_id match
            if session_id != expected_session_id:
                logger.warning(
                    f"MMIT LEAK DETECTED: Memory {memory.id} has wrong session_id "
                    f"({session_id} != expected {expected_session_id})"
                )
                leaks_detected += 1
                continue

            validated.append(memory)

        if leaks_detected > 0:
            logger.error(
                f"MMIT Isolation Violation: Blocked {leaks_detected} leaking memories "
                f"for agent {expected_agent_id}"
            )
            if raise_on_leak:
                from ..exceptions.base import RAEError
                raise RAEError(f"Security Violation: Cross-agent memory leak detected ({leaks_detected} items)")

        return validated