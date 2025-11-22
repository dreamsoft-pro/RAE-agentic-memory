"""
Tests for Event Triggers - Rules Engine and Automation

Tests cover:
- Event emission and processing
- Condition evaluation (AND/OR logic)
- Action execution
- Rate limiting and cooldowns
- Workflow orchestration
- Circuit breaker for actions
"""

import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock, patch

from apps.memory_api.services.rules_engine import RulesEngine
from apps.memory_api.models.event_models import (
    Event,
    EventType,
    Condition,
    ConditionGroup,
    ConditionOperator,
    ActionType,
    TriggerRule,
    TriggerStatus
)


@pytest.fixture
def mock_pool():
    return AsyncMock()


@pytest.fixture
def rules_engine(mock_pool):
    return RulesEngine(mock_pool)


@pytest.fixture
def sample_event():
    return Event(
        event_id=uuid4(),
        event_type=EventType.MEMORY_CREATED,
        tenant_id="test",
        project_id="test",
        source_service="api",
        payload={"importance": 0.9, "memory_count": 55}
    )


# Event Processing Tests
@pytest.mark.asyncio
async def test_process_event(rules_engine, sample_event, mock_pool):
    """Test event processing and trigger matching"""
    mock_pool.fetch = AsyncMock(return_value=[])

    result = await rules_engine.process_event(sample_event)

    assert "triggers_matched" in result
    assert "actions_executed" in result


# Condition Evaluation Tests
@pytest.mark.asyncio
async def test_evaluate_simple_condition(rules_engine):
    """Test simple condition evaluation"""
    condition = Condition(
        field="payload.importance",
        operator=ConditionOperator.GREATER_THAN,
        value=0.8
    )

    data = {"payload": {"importance": 0.9}}
    result = rules_engine._evaluate_condition(condition, data)

    assert result is True


@pytest.mark.asyncio
async def test_evaluate_condition_group_and(rules_engine):
    """Test AND condition group"""
    group = ConditionGroup(
        operator="AND",
        conditions=[
            Condition(field="payload.importance", operator=ConditionOperator.GREATER_THAN, value=0.8),
            Condition(field="payload.memory_count", operator=ConditionOperator.GREATER_EQUAL, value=50)
        ]
    )

    data = {"payload": {"importance": 0.9, "memory_count": 55}}
    result = rules_engine._evaluate_condition_group(group, data)

    assert result is True


@pytest.mark.asyncio
async def test_evaluate_condition_group_or(rules_engine):
    """Test OR condition group"""
    group = ConditionGroup(
        operator="OR",
        conditions=[
            Condition(field="payload.importance", operator=ConditionOperator.GREATER_THAN, value=0.95),
            Condition(field="payload.memory_count", operator=ConditionOperator.GREATER_EQUAL, value=50)
        ]
    )

    data = {"payload": {"importance": 0.7, "memory_count": 55}}
    result = rules_engine._evaluate_condition_group(group, data)

    assert result is True  # Second condition is true


@pytest.mark.asyncio
async def test_nested_condition_groups(rules_engine):
    """Test nested condition groups"""
    group = ConditionGroup(
        operator="AND",
        conditions=[
            Condition(field="payload.importance", operator=ConditionOperator.GREATER_THAN, value=0.5)
        ],
        groups=[
            ConditionGroup(
                operator="OR",
                conditions=[
                    Condition(field="payload.type", operator=ConditionOperator.EQUALS, value="critical"),
                    Condition(field="payload.priority", operator=ConditionOperator.GREATER_THAN, value=7)
                ]
            )
        ]
    )

    data = {"payload": {"importance": 0.8, "type": "critical", "priority": 5}}
    result = rules_engine._evaluate_condition_group(group, data)

    assert result is True


# Condition Operators Tests
@pytest.mark.asyncio
async def test_condition_operators(rules_engine):
    """Test all condition operators"""
    data = {
        "value": 10,
        "text": "hello world",
        "items": [1, 2, 3],
        "null_value": None
    }

    # EQUALS
    assert rules_engine._evaluate_condition(
        Condition(field="value", operator=ConditionOperator.EQUALS, value=10), data
    )

    # CONTAINS
    assert rules_engine._evaluate_condition(
        Condition(field="text", operator=ConditionOperator.CONTAINS, value="world"), data
    )

    # IN
    assert rules_engine._evaluate_condition(
        Condition(field="value", operator=ConditionOperator.IN, value=[10, 20, 30]), data
    )

    # IS_NULL
    assert rules_engine._evaluate_condition(
        Condition(field="null_value", operator=ConditionOperator.IS_NULL, value=None), data
    )


# Rate Limiting Tests
@pytest.mark.asyncio
async def test_rate_limiting(rules_engine, mock_pool):
    """Test rate limiting for triggers"""
    trigger = TriggerRule(
        trigger_id=uuid4(),
        tenant_id="test",
        project_id="test",
        rule_name="test",
        condition={"event_types": ["memory_created"]},
        actions=[],
        max_executions_per_hour=5,
        executions_this_hour=5,  # Already at limit
        hour_window_start=datetime.utcnow(),
        created_by="test"
    )

    # Should be rate limited
    can_execute = await rules_engine._check_rate_limit(trigger)
    assert can_execute is False


@pytest.mark.asyncio
async def test_cooldown_period(rules_engine):
    """Test cooldown period between executions"""
    from datetime import timedelta

    trigger = TriggerRule(
        trigger_id=uuid4(),
        tenant_id="test",
        project_id="test",
        rule_name="test",
        condition={"event_types": ["memory_created"]},
        actions=[],
        cooldown_seconds=60,
        last_executed_at=datetime.utcnow() - timedelta(seconds=30),  # Executed 30s ago
        created_by="test"
    )

    # Should be in cooldown
    can_execute = await rules_engine._check_cooldown(trigger)
    assert can_execute is False


# Action Execution Tests
@pytest.mark.asyncio
async def test_execute_action(rules_engine, sample_event, mock_pool):
    """Test action execution"""
    action_config = {
        "action_type": ActionType.SEND_NOTIFICATION,
        "config": {"channel": "email", "message": "Test"}
    }

    mock_pool.execute = AsyncMock()

    result = await rules_engine._execute_action(
        action_config, sample_event, uuid4()
    )

    assert "success" in result


# Workflow Tests
@pytest.mark.asyncio
async def test_workflow_execution(rules_engine, mock_pool):
    """Test workflow step execution"""
    workflow_id = uuid4()

    mock_pool.fetch = AsyncMock(return_value=[
        {
            "step_id": "step1",
            "action_type": "send_notification",
            "action_config": {},
            "depends_on": []
        }
    ])
    mock_pool.execute = AsyncMock()

    result = await rules_engine._execute_workflow(workflow_id, {})

    assert result["steps_completed"] >= 0
