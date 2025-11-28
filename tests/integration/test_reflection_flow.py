"""
Integration tests for Reflective Memory V1 Flow.

Tests the complete Actor → Evaluator → Reflector pattern:
1. Actor executes task with tool errors
2. Evaluator marks as failure
3. Reflector generates reflection
4. Reflection is stored in memory
5. Next execution retrieves reflection in context
"""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from apps.memory_api.models.reflection_v2_models import (
    ErrorCategory,
    ErrorInfo,
    Event,
    EventType,
    OutcomeType,
    ReflectionContext,
)
from apps.memory_api.services.reflection_engine_v2 import ReflectionEngineV2
from apps.memory_api.services.context_builder import ContextBuilder, ContextConfig
from apps.memory_api.services.memory_scoring_v2 import compute_memory_score
from apps.memory_api.repositories.memory_repository import MemoryRepository


pytestmark = pytest.mark.integration


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
async def db_pool(postgresql_pool):
    """Database connection pool"""
    return postgresql_pool


@pytest.fixture
async def memory_repo(db_pool):
    """Memory repository"""
    return MemoryRepository(db_pool)


@pytest.fixture
async def reflection_engine(db_pool, memory_repo):
    """Reflection engine v2"""
    return ReflectionEngineV2(db_pool, memory_repo)


@pytest.fixture
async def context_builder(db_pool, memory_repo, reflection_engine):
    """Context builder"""
    config = ContextConfig(
        max_reflection_items=5,
        min_reflection_importance=0.5,
        enable_enhanced_scoring=True,
    )
    return ContextBuilder(db_pool, memory_repo, reflection_engine, config)


@pytest.fixture
def tenant_id():
    """Test tenant ID"""
    return "test-tenant-" + str(uuid4())


@pytest.fixture
def project_id():
    """Test project ID"""
    return "test-project"


# ============================================================================
# Test: Failure Reflection Generation
# ============================================================================


@pytest.mark.asyncio
async def test_generate_reflection_from_failure(
    reflection_engine, memory_repo, tenant_id, project_id
):
    """
    Test reflection generation from a failed task execution.

    Scenario:
    1. Task fails with SQL timeout error
    2. Reflection engine generates lesson learned
    3. Reflection is stored with proper importance/confidence
    """
    # 1. Create failure context
    events = [
        Event(
            event_id="evt_1",
            event_type=EventType.TOOL_CALL,
            timestamp=datetime.now(timezone.utc),
            content="Executing SQL query: SELECT * FROM large_table",
            metadata={"tool": "sql_executor"},
            tool_name="sql_executor",
        ),
        Event(
            event_id="evt_2",
            event_type=EventType.ERROR_EVENT,
            timestamp=datetime.now(timezone.utc),
            content="Query timeout after 30 seconds",
            metadata={"error_code": "TIMEOUT"},
            error={"type": "TimeoutError", "code": "QUERY_TIMEOUT"},
        ),
    ]

    error_info = ErrorInfo(
        error_code="QUERY_TIMEOUT",
        error_category=ErrorCategory.TIMEOUT_ERROR,
        error_message="SQL query timeout after 30 seconds",
        tool_name="sql_executor",
        context={"query": "SELECT * FROM large_table", "timeout_seconds": 30},
    )

    context = ReflectionContext(
        events=events,
        outcome=OutcomeType.FAILURE,
        error=error_info,
        task_description="Fetch data from large table",
        task_goal="Retrieve user analytics data",
        tenant_id=tenant_id,
        project_id=project_id,
    )

    # 2. Generate reflection
    result = await reflection_engine.generate_reflection(context)

    # 3. Assertions on reflection result
    assert result is not None
    assert len(result.reflection_text) > 0, "Reflection text should not be empty"
    assert result.importance > 0.3, "Failure reflection should have reasonable importance"
    assert result.confidence > 0.0, "Confidence should be non-zero"
    assert result.error_category == ErrorCategory.TIMEOUT_ERROR
    assert len(result.source_event_ids) == len(events)

    # Check for relevant tags
    assert any(
        tag.lower() in ["sql", "timeout", "performance", "query"]
        for tag in result.tags
    ), "Reflection should have relevant tags"

    # 4. Store reflection
    stored_ids = await reflection_engine.store_reflection(
        result=result,
        tenant_id=tenant_id,
        project_id=project_id,
    )

    assert "reflection_id" in stored_ids
    assert stored_ids["reflection_id"] is not None

    # 5. Verify stored in database
    reflections = await memory_repo.get_reflective_memories(
        tenant_id=tenant_id, project=project_id
    )
    assert len(reflections) >= 1, "Reflection should be stored in database"

    # Find our reflection
    our_reflection = next(
        (r for r in reflections if r["id"] == stored_ids["reflection_id"]), None
    )
    assert our_reflection is not None
    assert our_reflection["content"] == result.reflection_text
    assert our_reflection["importance"] == result.importance


# ============================================================================
# Test: Success Reflection Generation
# ============================================================================


@pytest.mark.asyncio
async def test_generate_reflection_from_success(
    reflection_engine, memory_repo, tenant_id, project_id
):
    """
    Test reflection generation from a successful task execution.

    Scenario:
    1. Task succeeds with optimization
    2. Reflection engine generates positive pattern
    3. Reflection stored as reusable strategy
    """
    events = [
        Event(
            event_id="evt_1",
            event_type=EventType.TOOL_CALL,
            timestamp=datetime.now(timezone.utc),
            content="Executing optimized SQL query: SELECT id, name FROM users LIMIT 100",
            metadata={"tool": "sql_executor", "optimization": "added_limit"},
            tool_name="sql_executor",
        ),
        Event(
            event_id="evt_2",
            event_type=EventType.TOOL_RESPONSE,
            timestamp=datetime.now(timezone.utc),
            content="Query completed successfully in 0.5 seconds",
            metadata={"execution_time_ms": 500},
        ),
    ]

    context = ReflectionContext(
        events=events,
        outcome=OutcomeType.SUCCESS,
        task_description="Fetch user data efficiently",
        task_goal="Retrieve first 100 users",
        tenant_id=tenant_id,
        project_id=project_id,
    )

    # Generate reflection
    result = await reflection_engine.generate_reflection(context)

    assert result is not None
    assert len(result.reflection_text) > 0
    assert result.importance >= 0.0, "Success reflection should have some importance"

    # Success reflections might have strategy
    if result.strategy_text:
        assert len(result.strategy_text) > 0
        # Store should create both reflection and strategy
        stored_ids = await reflection_engine.store_reflection(
            result=result, tenant_id=tenant_id, project_id=project_id
        )
        assert "strategy_id" in stored_ids


# ============================================================================
# Test: Reflection Retrieval in Context
# ============================================================================


@pytest.mark.asyncio
async def test_reflection_retrieval_in_context(
    reflection_engine,
    context_builder,
    memory_repo,
    tenant_id,
    project_id,
):
    """
    Test that reflections are retrieved and injected into context.

    Scenario:
    1. Store a reflection about SQL timeouts
    2. Build context for a new SQL query task
    3. Verify reflection is included in context
    """
    # 1. Store a reflection manually
    reflection_content = (
        "SQL queries on large tables should always include LIMIT clause "
        "to prevent timeout errors. Default timeout is 30 seconds."
    )

    reflection_record = await memory_repo.insert_memory(
        tenant_id=tenant_id,
        content=reflection_content,
        source="test",
        importance=0.8,
        layer="rm",
        tags=["sql", "timeout", "best-practice"],
        timestamp=datetime.now(timezone.utc),
        project=project_id,
    )

    # 2. Build context with query about SQL
    query = "I need to fetch all user data from the users table"

    working_memory = await context_builder.build_context(
        tenant_id=tenant_id,
        project_id=project_id,
        query=query,
        recent_messages=[],
    )

    # 3. Verify reflection is in context
    assert len(working_memory.reflections) >= 1, "Should retrieve reflections"

    # Check our reflection is included (by content or ID)
    reflection_found = any(
        refl.metadata.get("id") == reflection_record["id"]
        for refl in working_memory.reflections
    )
    assert reflection_found, "Our test reflection should be in context"

    # 4. Verify formatted context includes lessons learned
    assert "Lessons Learned" in working_memory.context_text or "lessons learned" in working_memory.context_text.lower(), \
        "Context should include lessons learned section"

    # 5. Verify reflection content is in formatted text
    # (It should be in the Lessons Learned section)
    assert any(
        reflection_content in refl.content
        for refl in working_memory.reflections
    ), "Reflection content should be accessible"


# ============================================================================
# Test: Memory Scoring V2
# ============================================================================


@pytest.mark.asyncio
async def test_memory_scoring_v2():
    """
    Test enhanced memory scoring function.

    Tests the unified Relevance + Importance + Recency scoring.
    """
    # Recent, high-importance, high-relevance memory
    score1 = compute_memory_score(
        similarity=0.9,
        importance=0.8,
        last_accessed_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        access_count=10,
        memory_id="mem_1",
    )

    # Old, low-importance, medium-relevance memory
    old_date = datetime.now(timezone.utc).replace(year=2023)
    score2 = compute_memory_score(
        similarity=0.6,
        importance=0.3,
        last_accessed_at=old_date,
        created_at=old_date,
        access_count=1,
        memory_id="mem_2",
    )

    # Score 1 should be significantly higher
    assert score1.final_score > score2.final_score, "Recent high-importance should score higher"

    # Verify component breakdown
    assert score1.relevance_score == 0.9
    assert score1.importance_score == 0.8
    assert score1.recency_score > 0.9, "Recent memory should have high recency"

    assert score2.recency_score < 0.1, "Old memory should have low recency"


# ============================================================================
# Test: Context Injection
# ============================================================================


@pytest.mark.asyncio
async def test_inject_reflections_into_prompt(
    context_builder, memory_repo, tenant_id, project_id
):
    """
    Test the helper method for injecting reflections into existing prompts.
    """
    # 1. Store a reflection
    await memory_repo.insert_memory(
        tenant_id=tenant_id,
        content="Always validate user input before processing",
        source="test",
        importance=0.9,
        layer="rm",
        tags=["security", "validation"],
        timestamp=datetime.now(timezone.utc),
        project=project_id,
    )

    # 2. Inject into prompt
    base_prompt = "You are a helpful assistant."
    enhanced_prompt = await context_builder.inject_reflections_into_prompt(
        base_prompt=base_prompt,
        tenant_id=tenant_id,
        project_id=project_id,
        query="How should I handle user input?",
    )

    # 3. Verify injection
    assert len(enhanced_prompt) > len(base_prompt), "Prompt should be enhanced"
    assert "Lessons Learned" in enhanced_prompt or "lessons learned" in enhanced_prompt.lower(), \
        "Should include lessons learned section"
    assert "validate user input" in enhanced_prompt.lower(), "Should include reflection content"


# ============================================================================
# Test: End-to-End Flow
# ============================================================================


@pytest.mark.asyncio
async def test_end_to_end_reflection_flow(
    reflection_engine,
    context_builder,
    memory_repo,
    tenant_id,
    project_id,
):
    """
    Test complete end-to-end flow:
    1. Task fails with error
    2. Reflection generated and stored
    3. Next task retrieves reflection
    4. Reflection influences behavior
    """
    # === Phase 1: First execution fails ===

    # Simulate tool error
    events_fail = [
        Event(
            event_id="evt_1",
            event_type=EventType.TOOL_CALL,
            timestamp=datetime.now(timezone.utc),
            content="Calling API without authentication header",
            metadata={"tool": "http_client"},
            tool_name="http_client",
        ),
        Event(
            event_id="evt_2",
            event_type=EventType.ERROR_EVENT,
            timestamp=datetime.now(timezone.utc),
            content="401 Unauthorized",
            metadata={"error_code": "UNAUTHORIZED"},
            error={"type": "AuthError", "code": "401"},
        ),
    ]

    error = ErrorInfo(
        error_code="401",
        error_category=ErrorCategory.PERMISSION_ERROR,
        error_message="API call failed: 401 Unauthorized",
        tool_name="http_client",
    )

    context_fail = ReflectionContext(
        events=events_fail,
        outcome=OutcomeType.FAILURE,
        error=error,
        task_description="Call external API",
        task_goal="Fetch data from API",
        tenant_id=tenant_id,
        project_id=project_id,
    )

    # Generate and store reflection
    result = await reflection_engine.generate_reflection(context_fail)
    stored_ids = await reflection_engine.store_reflection(
        result=result, tenant_id=tenant_id, project_id=project_id
    )

    reflection_id = stored_ids["reflection_id"]
    assert reflection_id is not None

    # === Phase 2: Second execution retrieves lesson ===

    # Build context for similar task
    query = "I need to call the external API again"
    working_memory = await context_builder.build_context(
        tenant_id=tenant_id, project_id=project_id, query=query
    )

    # Verify reflection is available
    assert len(working_memory.reflections) >= 1, "Should retrieve previous reflection"

    # Check if our reflection is there
    our_refl = next(
        (r for r in working_memory.reflections if r.metadata.get("id") == reflection_id),
        None,
    )
    assert our_refl is not None, "Our reflection should be retrieved"

    # === Phase 3: Verify reflection is actionable ===

    # The reflection should mention authentication or auth header
    assert any(
        keyword in our_refl.content.lower()
        for keyword in ["auth", "unauthorized", "401", "header", "token"]
    ), "Reflection should mention authentication issue"

    # If strategy was generated, it should be actionable
    if result.strategy_text:
        assert len(result.strategy_text) > 10, "Strategy should be meaningful"
