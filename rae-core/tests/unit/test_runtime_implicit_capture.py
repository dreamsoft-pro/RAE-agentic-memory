from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from rae_core.interfaces.agent import BaseAgent
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.models.interaction import AgentAction, AgentActionType, RAEInput
from rae_core.runtime import RAERuntime

class ToolUsingAgent(BaseAgent):
    async def run(self, input_payload: RAEInput) -> AgentAction:
        return AgentAction(
            type=AgentActionType.TOOL_CALL,
            content="read_file('secret.txt')",
            confidence=1.0,
            reasoning="Checking secrets",
            signals=["critical"]
        )

class ThinkingAgent(BaseAgent):
    async def run(self, input_payload: RAEInput) -> AgentAction:
        return AgentAction(
            type=AgentActionType.THOUGHT,
            content="I should check the database.",
            confidence=0.8,
            reasoning="Planning next step",
            signals=["decision"]
        )

@pytest.mark.asyncio
async def test_implicit_capture_tool_call():
    """Test that TOOL_CALL is implicitly captured in Working memory."""
    storage = MagicMock(spec=IMemoryStorage)
    storage.store_memory = AsyncMock()

    agent = ToolUsingAgent()
    runtime = RAERuntime(storage, agent)

    session_id = str(uuid4())
    payload = RAEInput(
        request_id=uuid4(),
        tenant_id="test-tenant",
        content="Do something risky",
        context={"project": "test-project", "session_id": session_id},
    )

    await runtime.process(payload)

    # Verify memory hook
    storage.store_memory.assert_called_once()
    call_args = storage.store_memory.call_args[1]
    
    # Should be in WORKING layer (audit trail)
    assert call_args["layer"] == "working"
    assert "Tool Call: read_file('secret.txt')" in call_args["content"]
    assert "audit" in call_args["tags"]
    assert "tool_call" in call_args["tags"]
    assert call_args["session_id"] == session_id
    assert call_args["source"] == "RAERuntime"

@pytest.mark.asyncio
async def test_implicit_capture_thought():
    """Test that THOUGHT/DECISION is implicitly captured in Working memory."""
    storage = MagicMock(spec=IMemoryStorage)
    storage.store_memory = AsyncMock()

    agent = ThinkingAgent()
    runtime = RAERuntime(storage, agent)

    session_id = str(uuid4())
    payload = RAEInput(
        request_id=uuid4(),
        tenant_id="test-tenant",
        content="Think about it",
        context={"project": "test-project", "session_id": session_id},
    )

    await runtime.process(payload)

    # Verify memory hook
    storage.store_memory.assert_called_once()
    call_args = storage.store_memory.call_args[1]
    
    assert call_args["layer"] == "working"
    assert "Planning next step" in call_args["content"]
    assert "trace" in call_args["tags"]
    assert call_args["session_id"] == session_id
