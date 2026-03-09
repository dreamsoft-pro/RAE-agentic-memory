"""Unit tests for agent output contracts."""

import pytest
from pydantic import ValidationError
from rae_core.models.contracts import (
    AgentDecision,
    AgentOutputContract,
    ContractValidationResult
)

def test_agent_decision_enum():
    assert AgentDecision.PROCEED == "proceed"
    assert AgentDecision.ABORT == "abort"

def test_agent_output_contract_valid():
    contract = AgentOutputContract(
        analysis="This is a deep reasoning analysis that is long enough.",
        decision=AgentDecision.PROCEED,
        confidence=0.95,
        retrieved_sources=["mem1", "mem2"],
        metadata={"model": "qwen-14b"}
    )
    assert contract.decision == "proceed"
    assert len(contract.retrieved_sources) == 2

def test_agent_output_contract_invalid_analysis():
    with pytest.raises(ValidationError):
        # Analysis too short
        AgentOutputContract(
            analysis="Short",
            decision=AgentDecision.PROCEED,
            confidence=0.9,
            retrieved_sources=["mem1"]
        )

def test_agent_output_contract_invalid_confidence():
    with pytest.raises(ValidationError):
        # Confidence out of range
        AgentOutputContract(
            analysis="Valid length analysis string here.",
            decision=AgentDecision.PROCEED,
            confidence=1.5,
            retrieved_sources=["mem1"]
        )

def test_agent_output_contract_missing_sources():
    with pytest.raises(ValidationError, match="List should have at least 1 item"):
        # Empty sources
        AgentOutputContract(
            analysis="Valid length analysis string here.",
            decision=AgentDecision.PROCEED,
            confidence=0.9,
            retrieved_sources=[]
        )

def test_contract_validation_result_default():
    res = ContractValidationResult()
    assert res.is_valid is False
    assert res.block_reasons == []

def test_contract_validation_result_valid():
    res = ContractValidationResult(is_valid=True, audit_trace_id="trace-123")
    assert res.is_valid is True
    assert res.audit_trace_id == "trace-123"
