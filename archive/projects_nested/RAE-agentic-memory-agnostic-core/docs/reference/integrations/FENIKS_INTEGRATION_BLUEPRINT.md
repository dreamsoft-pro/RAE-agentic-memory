# RAE ↔ Feniks: Blueprint Pełnej Synergicznej Integracji

**Wersja:** 1.0
**Data:** 2025-11-29
**Status:** Architecture Design
**Autor:** RAE Team + Feniks Team

---

## 🎯 Executive Summary

Ten dokument opisuje **pełną, synergiczną integrację** między RAE (Reflective Agentic Memory Engine) a Feniksem (Enterprise Code Analysis & Refactoring System). Nie jest to zwykłe "podłączenie API" - to **architektura dwukierunkowej synergii**, gdzie oba systemy wzajemnie się wzbogacają i uczą.

### Kluczowe Osiągnięcia Integracji:

- ✅ **Dual-Memory Architecture**: RAE + Qdrant działają synergicznie, nie konkurencyjnie
- ✅ **Intelligent Memory Router**: Smart routing między lokalnymi a globalnymi pamięciami
- ✅ **4-Layer Bi-directional Flow**: Episodic → Working → Semantic → LTM w obu kierunkach
- ✅ **Reflection Enrichment Loop**: Feniks insights → RAE reflection → Enhanced Feniks decisions
- ✅ **Multi-Project Learning**: Wiedza z jednego projektu wspiera inne (via RAE)

---

## 📊 Część 1: Analiza Obecnego Stanu

### 1.1. Architektura Feniksa (Clean Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    FENIKS ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  APPS LAYER (Entry Points)                         │    │
│  │  • CLI (feniks command)                            │    │
│  │  • REST API (FastAPI)                              │    │
│  │  • Async Workers (Celery-like)                     │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  CORE LAYER (Business Logic)                       │    │
│  │  • MetaReflectionEngine - generates insights       │    │
│  │  • AnalysisPipeline - system model builder         │    │
│  │  • RefactorEngine - recipe-based transformations   │    │
│  │  • PolicyManager - budget & quality rules          │    │
│  │  • Behavior Guard - regression detection           │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  ADAPTERS LAYER (Infrastructure)                   │    │
│  │  • Storage (Qdrant) - vector embeddings           │    │
│  │  • RAE Client - basic write-only integration      │    │
│  │  • Ingest (Loaders) - code parsing                │    │
│  │  • LLM (Embeddings) - multi-model support         │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Kluczowe Komponenty Feniksa:**

1. **MetaReflectionEngine** (`feniks/core/reflection/engine.py`)
   - Generuje meta-refleksje o jakości kodu
   - Używa rule-based system + LLM
   - Outputy: MetaReflection objects (JSONL)

2. **Obecny RAEClient** (`feniks/adapters/rae_client/client.py`)
   - **Write-only**: store_meta_reflection(), store_system_capabilities()
   - Brak read operations
   - Brak synchronizacji zwrotnej

3. **Qdrant Storage** (`feniks/adapters/storage/`)
   - Przechowuje embeddingi code chunks
   - Semantic search w obrębie projektu
   - **Lokalne** - nie współdzieli między projektami

### 1.2. Architektura RAE (4-Layer Memory)

```
┌─────────────────────────────────────────────────────────────┐
│                     RAE ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LAYER 1: EPISODIC MEMORY                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Recent events, refactorings, decisions            │    │
│  │  Retention: Hours to Days                          │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  LAYER 2: WORKING MEMORY                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Active task context + reflections                 │    │
│  │  Retention: Current session                        │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  LAYER 3: SEMANTIC MEMORY (LTM)                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Facts, patterns, principles                       │    │
│  │  Retention: Weeks to Months                        │    │
│  │  GraphRAG: Knowledge graph connections             │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  LAYER 4: REFLECTIVE MEMORY (Meta-Level)                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Meta-learnings, strategies, wisdom                │    │
│  │  Retention: Permanent                              │    │
│  │  ReflectionEngineV2: Actor-Evaluator-Reflector     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  CROSS-CUTTING:                                             │
│  • HybridSearchService - multi-strategy retrieval           │
│  • TemporalGraph - time-aware connections                   │
│  • CostController - budget management                       │
│  • Multi-tenant - project isolation                         │
└─────────────────────────────────────────────────────────────┘
```

**Kluczowe Usługi RAE:**

1. **ReflectionEngineV2** - Actor-Evaluator-Reflector pattern
2. **HybridSearchService** - Vector + Graph + Fulltext
3. **GraphRAG** - Knowledge graph z entity resolution
4. **Multi-Model LLM Router** - 7 providerów (OpenAI, Anthropic, Gemini, Ollama, etc.)

### 1.3. Gap Analysis - Czego Brakuje?

| Feature | Feniks Obecny | RAE | Gap |
|---------|---------------|-----|-----|
| **Multi-project learning** | ❌ Isolated per-project | ✅ Cross-project insights | **CRITICAL** |
| **Bidirectional sync** | ❌ Write-only to RAE | ✅ Read/write | **CRITICAL** |
| **Temporal evolution** | ❌ Snapshot-based | ✅ Time-aware graph | **HIGH** |
| **Reflection enrichment** | ❌ Static rules | ✅ LLM-powered learning | **HIGH** |
| **Knowledge graph** | ❌ Flat vectors | ✅ GraphRAG entities | **MEDIUM** |
| **Cross-project patterns** | ❌ No sharing | ✅ Semantic clustering | **MEDIUM** |
| **Meta-level insights** | ⚠️ Basic self-model | ✅ Full meta-reflection | **LOW** |

---

## 🏗️ Część 2: Architektura Synergiczna

### 2.1. Filozofia: Dual-Memory Strategy

**NIE**: Zastępowanie Qdrant przez RAE
**TAK**: Synergiczne wykorzystanie obu systemów

```
╔══════════════════════════════════════════════════════════════╗
║              DUAL-MEMORY SYNERGY PHILOSOPHY                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  QDRANT (Feniks Local)          RAE (Global Shared)         ║
║  ┌─────────────────────┐        ┌──────────────────────┐    ║
║  │ • Fast local search │        │ • Cross-project      │    ║
║  │ • Project-specific  │  ←→    │ • Temporal evolution │    ║
║  │ • Code embeddings   │        │ • Meta-reflections   │    ║
║  │ • Immediate recall  │        │ • Pattern learning   │    ║
║  └─────────────────────┘        └──────────────────────┘    ║
║           ↓                              ↓                   ║
║     FAST RETRIEVAL              INTELLIGENT INSIGHTS         ║
║                                                              ║
║  WHEN TO USE QDRANT:           WHEN TO USE RAE:             ║
║  • Semantic search in code     • Historical decisions       ║
║  • Finding similar chunks      • Cross-project patterns     ║
║  • Quick local lookups         • Reflection enrichment      ║
║  • Real-time analysis          • Long-term learning         ║
╚══════════════════════════════════════════════════════════════╝
```

### 2.2. Intelligent Memory Router

**Nowy komponent**: `FeniksMemoryRouter`

```python
class FeniksMemoryRouter:
    """
    Routes memory operations between Qdrant (local) and RAE (global).

    Decision Matrix:
    - Code chunks → Qdrant (fast semantic search)
    - Meta-reflections → RAE (learning & evolution)
    - Refactor decisions → BOTH (local cache + global memory)
    - System capabilities → RAE (cross-project insights)
    - Architectural patterns → RAE (GraphRAG connections)
    """

    def store(self, data: MemoryItem) -> MemoryRouterResult:
        """Smart routing based on data type and metadata."""

        if data.type == "code_chunk":
            # Local Qdrant for fast retrieval
            qdrant_id = self.qdrant.store(data)
            return MemoryRouterResult(primary=qdrant_id, secondary=None)

        elif data.type == "meta_reflection":
            # RAE for learning and evolution
            rae_id = self.rae.store_reflection(data)
            return MemoryRouterResult(primary=rae_id, secondary=None)

        elif data.type == "refactor_decision":
            # BOTH - local cache + global learning
            qdrant_id = self.qdrant.store(data)
            rae_id = self.rae.store_episodic(data)
            return MemoryRouterResult(primary=qdrant_id, secondary=rae_id)

        elif data.type == "system_capability":
            # RAE for cross-project insights
            rae_id = self.rae.store_semantic(data)
            return MemoryRouterResult(primary=rae_id, secondary=None)

    def retrieve(self, query: MemoryQuery) -> List[MemoryItem]:
        """Smart retrieval combining both sources."""

        results = []

        # Strategy 1: Fast local search (Qdrant)
        if query.requires_fast_response:
            local_results = self.qdrant.search(query)
            results.extend(local_results)

        # Strategy 2: Deep insights (RAE)
        if query.requires_insights:
            rae_results = self.rae.query_with_reflection(query)
            results.extend(rae_results)

        # Strategy 3: Hybrid (combine & re-rank)
        if query.requires_best_of_both:
            local = self.qdrant.search(query, top_k=20)
            global_insights = self.rae.query(query, top_k=10)
            results = self._hybrid_rerank(local, global_insights)

        return results
```

### 2.3. Data Flow: 4-Layer Bi-directional Integration

```
┌────────────────────────────────────────────────────────────────┐
│                    FENIKS ↔ RAE DATA FLOW                      │
└────────────────────────────────────────────────────────────────┘

PHASE 1: CODE ANALYSIS (Feniks → RAE)
════════════════════════════════════════════════════════════════
   Feniks Ingest Pipeline
           │
           ├─→ Parse code chunks → Qdrant (local embeddings)
           │
           └─→ Generate meta-reflections
                    │
                    ├─→ RAE EPISODIC: Recent refactoring events
                    │   • What: "Extracted UserService from monolith"
                    │   • When: timestamp
                    │   • Why: "Reduce complexity, improve testability"
                    │
                    ├─→ RAE SEMANTIC: System capabilities
                    │   • "Has authentication module with JWT"
                    │   • "Uses React for UI components"
                    │   • GraphRAG: links to similar projects
                    │
                    └─→ RAE REFLECTIVE: Meta-level insights
                        • "This codebase favors composition over inheritance"
                        • "High test coverage correlates with fewer bugs"

PHASE 2: REFLECTION ENRICHMENT (RAE → Feniks)
════════════════════════════════════════════════════════════════
   RAE Reflection Engine V2
           │
           ├─→ Actor: Generate new insights from Feniks data
           │   • "Similar pattern seen in Project X (successful)"
           │   • "This refactoring reduced complexity by 40%"
           │
           ├─→ Evaluator: Assess Feniks decisions
           │   • "High confidence - matches learned patterns"
           │   • "Warning: This pattern failed in Project Y"
           │
           └─→ Reflector: Meta-learnings
                    │
                    └─→ Feniks MetaReflectionEngine
                        • Enhanced recommendations
                        • Cross-project insights
                        • Confidence scores based on history

PHASE 3: DECISION MAKING (Feniks uses RAE insights)
════════════════════════════════════════════════════════════════
   Feniks RefactorEngine
           │
           ├─→ Query RAE: "Similar refactorings for Angular→React"
           │   • RAE returns: 15 past migrations with outcomes
           │   • Success rate: 80% (12/15 successful)
           │   • Common pitfalls: State management, routing
           │
           ├─→ FeniksMemoryRouter combines:
           │   • Local Qdrant: Current project code chunks
           │   • RAE insights: Historical patterns & outcomes
           │
           └─→ Generate refactoring plan
                    │
                    └─→ Store decision back to RAE (episodic)

PHASE 4: LEARNING LOOP (Continuous Improvement)
════════════════════════════════════════════════════════════════
   Post-Refactoring Feedback
           │
           ├─→ Feniks Behavior Guard: Test results
           │   • Success: All tests pass
           │   • Failure: 3/50 tests failed
           │
           ├─→ Store outcome to RAE (episodic + semantic)
           │   • "Angular→React migration: SUCCESS"
           │   • Tags: [angular, react, migration, success]
           │   • Lessons: [state-management-key, routing-tricky]
           │
           └─→ RAE Reflection Engine V2
                    │
                    ├─→ Update semantic memory
                    │   • "React migrations from Angular: 81% success (13/16)"
                    │   • Strengthen pattern: "Extract state first"
                    │
                    └─→ Generate meta-reflection
                        • "System improving: Angular migrations +5% success"
                        • Store to reflective layer (permanent learning)
```

---

## 🔧 Część 3: Implementacja Krok po Kroku

### 3.1. Enhanced RAE Client

**Lokalizacja**: `feniks/adapters/rae_client/enhanced_client.py`

```python
"""
Enhanced RAE Client - Bidirectional integration with full RAE capabilities.
Extends basic RAEClient with read operations, reflection enrichment, and smart routing.
"""
from typing import List, Dict, Any, Optional
from feniks.adapters.rae_client.client import RAEClient, RAEError
from feniks.core.models.types import MetaReflection, RefactorDecision
from feniks.infra.logging import get_logger

log = get_logger("adapters.rae_client.enhanced")


class EnhancedRAEClient(RAEClient):
    """
    Enhanced RAE client with bidirectional sync and intelligent retrieval.

    New Capabilities:
    - Read operations (query, search, retrieve)
    - Reflection enrichment (enhance local reflections with RAE insights)
    - Cross-project learning (find similar patterns)
    - Temporal queries (evolution over time)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}  # Simple in-memory cache
        log.info("EnhancedRAEClient initialized with bidirectional sync")

    # ========================================================================
    # READ OPERATIONS (New)
    # ========================================================================

    def query_reflections(
        self,
        project_id: str,
        query_text: str,
        layer: str = "semantic",
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Query RAE for relevant reflections.

        Args:
            project_id: Project identifier
            query_text: Natural language query
            layer: Memory layer (episodic, working, semantic, ltm)
            top_k: Number of results

        Returns:
            List of reflections with relevance scores
        """
        log.info(f"Querying RAE reflections: project={project_id}, layer={layer}")

        try:
            response = self._make_request(
                method="POST",
                endpoint="/v2/memories/query",
                data={
                    "query_text": query_text,
                    "project_id": project_id,
                    "layer": layer,
                    "k": top_k
                }
            )

            results = response.get("results", [])
            log.info(f"Retrieved {len(results)} reflections from RAE")
            return results

        except Exception as e:
            raise RAEError(f"Failed to query reflections: {e}") from e

    def get_cross_project_patterns(
        self,
        pattern_type: str,
        min_confidence: float = 0.7,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Retrieve cross-project patterns from RAE semantic memory.

        Args:
            pattern_type: Type of pattern (e.g., "refactoring", "architecture")
            min_confidence: Minimum confidence score
            limit: Maximum number of patterns

        Returns:
            List of patterns with metadata and confidence scores
        """
        log.info(f"Fetching cross-project patterns: type={pattern_type}")

        try:
            response = self._make_request(
                method="POST",
                endpoint="/v2/memories/patterns/search",
                data={
                    "pattern_type": pattern_type,
                    "min_confidence": min_confidence,
                    "limit": limit
                }
            )

            patterns = response.get("patterns", [])
            log.info(f"Retrieved {len(patterns)} cross-project patterns")
            return patterns

        except Exception as e:
            raise RAEError(f"Failed to fetch patterns: {e}") from e

    def get_historical_refactorings(
        self,
        refactor_type: str,
        project_tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get historical refactoring decisions and outcomes from RAE.

        Args:
            refactor_type: Type of refactoring (e.g., "extract_method", "angular_to_react")
            project_tags: Optional project tags for filtering
            limit: Maximum number of results

        Returns:
            List of historical refactorings with outcomes
        """
        log.info(f"Fetching historical refactorings: type={refactor_type}")

        try:
            params = {
                "refactor_type": refactor_type,
                "limit": limit
            }
            if project_tags:
                params["tags"] = ",".join(project_tags)

            response = self._make_request(
                method="GET",
                endpoint="/v2/memories/refactorings/history",
                params=params
            )

            refactorings = response.get("refactorings", [])

            # Calculate success rate
            total = len(refactorings)
            successful = sum(1 for r in refactorings if r.get("outcome") == "success")
            success_rate = (successful / total * 100) if total > 0 else 0

            log.info(f"Retrieved {total} refactorings, success rate: {success_rate:.1f}%")

            return refactorings

        except Exception as e:
            raise RAEError(f"Failed to fetch refactorings: {e}") from e

    # ========================================================================
    # REFLECTION ENRICHMENT (New)
    # ========================================================================

    def enrich_reflection(
        self,
        local_reflection: MetaReflection,
        context: Optional[Dict[str, Any]] = None
    ) -> MetaReflection:
        """
        Enrich local Feniks reflection with RAE insights.

        Process:
        1. Query RAE for similar reflections
        2. Get cross-project patterns
        3. Enhance recommendations with learned insights
        4. Add confidence scores based on historical data

        Args:
            local_reflection: Feniks-generated reflection
            context: Additional context (project tags, etc.)

        Returns:
            Enriched reflection with RAE insights
        """
        log.info(f"Enriching reflection: {local_reflection.id}")

        try:
            # Query RAE for similar reflections
            similar = self.query_reflections(
                project_id=local_reflection.project_id,
                query_text=local_reflection.content,
                layer="semantic",
                top_k=5
            )

            # Get relevant patterns
            patterns = []
            for tag in local_reflection.tags:
                project_patterns = self.get_cross_project_patterns(
                    pattern_type=tag,
                    min_confidence=0.7,
                    limit=3
                )
                patterns.extend(project_patterns)

            # Enhance recommendations
            enhanced_recommendations = local_reflection.recommendations.copy()

            for pattern in patterns[:3]:  # Top 3 patterns
                if pattern.get("recommendation"):
                    enhanced_recommendations.append(
                        f"[Cross-project insight] {pattern['recommendation']}"
                    )

            # Add RAE insights to metadata
            local_reflection.metadata["rae_enrichment"] = {
                "similar_reflections_count": len(similar),
                "cross_project_patterns": len(patterns),
                "confidence_adjustment": self._calculate_confidence_boost(similar, patterns),
                "enriched_at": datetime.now().isoformat()
            }

            local_reflection.recommendations = enhanced_recommendations
            local_reflection.confidence *= self._calculate_confidence_boost(similar, patterns)

            log.info(f"Reflection enriched with {len(similar)} similar + {len(patterns)} patterns")

            return local_reflection

        except Exception as e:
            log.warning(f"Failed to enrich reflection: {e}")
            return local_reflection  # Return original on error

    def _calculate_confidence_boost(
        self,
        similar_reflections: List[Dict],
        patterns: List[Dict]
    ) -> float:
        """Calculate confidence boost based on RAE insights."""
        base_boost = 1.0

        # More similar reflections = higher confidence
        if len(similar_reflections) > 3:
            base_boost += 0.1

        # High-confidence patterns = higher boost
        high_conf_patterns = [p for p in patterns if p.get("confidence", 0) > 0.8]
        if len(high_conf_patterns) > 0:
            base_boost += 0.15

        return min(base_boost, 1.3)  # Cap at 30% boost

    # ========================================================================
    # DECISION SUPPORT (New)
    # ========================================================================

    def get_refactor_recommendation(
        self,
        refactor_type: str,
        code_context: Dict[str, Any],
        project_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get AI-powered refactoring recommendation from RAE.

        Combines:
        - Historical refactoring outcomes
        - Similar code patterns
        - Project-specific context
        - Cross-project learnings

        Args:
            refactor_type: Type of refactoring to perform
            code_context: Current code state (complexity, dependencies, etc.)
            project_context: Project metadata (tags, size, tech stack)

        Returns:
            Recommendation with confidence, risks, and suggested approach
        """
        log.info(f"Getting refactor recommendation: {refactor_type}")

        try:
            response = self._make_request(
                method="POST",
                endpoint="/v1/agent/refactor/recommend",
                data={
                    "refactor_type": refactor_type,
                    "code_context": code_context,
                    "project_context": project_context
                }
            )

            recommendation = response.get("recommendation", {})

            log.info(
                f"RAE recommendation: confidence={recommendation.get('confidence')}, "
                f"risk={recommendation.get('risk_level')}"
            )

            return recommendation

        except Exception as e:
            raise RAEError(f"Failed to get recommendation: {e}") from e

    # ========================================================================
    # FEEDBACK LOOP (New)
    # ========================================================================

    def store_refactor_outcome(
        self,
        refactor_decision: RefactorDecision,
        outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Store refactoring outcome for learning.

        Creates feedback loop: Feniks executes → stores outcome → RAE learns

        Args:
            refactor_decision: Original refactoring decision
            outcome: Execution results (success, test results, metrics)

        Returns:
            Storage confirmation from RAE
        """
        log.info(f"Storing refactor outcome: {refactor_decision.id}")

        payload = {
            "refactor_id": refactor_decision.id,
            "refactor_type": refactor_decision.type,
            "project_id": refactor_decision.project_id,
            "outcome_status": outcome.get("status"),  # success, failure, partial
            "test_results": outcome.get("test_results"),
            "metrics_delta": outcome.get("metrics", {}),
            "lessons_learned": outcome.get("lessons", []),
            "timestamp": datetime.now().isoformat(),
            "source": "feniks-refactor-engine"
        }

        try:
            response = self.store_system_model(payload)  # Use existing method

            log.info(f"Refactor outcome stored: {refactor_decision.id}")
            return response

        except Exception as e:
            raise RAEError(f"Failed to store outcome: {e}") from e


# ========================================================================
# FACTORY FUNCTIONS
# ========================================================================

def create_enhanced_rae_client() -> Optional[EnhancedRAEClient]:
    """
    Factory function to create enhanced RAE client if enabled.

    Returns:
        Optional[EnhancedRAEClient]: Enhanced client or None if disabled
    """
    from feniks.config.settings import settings

    if not settings.rae_enabled:
        log.debug("RAE integration is disabled")
        return None

    try:
        client = EnhancedRAEClient(
            base_url=settings.rae_base_url,
            api_key=settings.rae_api_key,
            timeout=settings.rae_timeout
        )
        return client
    except RAEError as e:
        log.warning(f"Failed to create enhanced RAE client: {e}")
        return None
```

---

## 📈 Część 4: Use Cases & Workflows

### Use Case 1: Cross-Project Refactoring Insights

**Scenario**: Feniks analizuje projekt Angular i proponuje migrację do React.

```
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOW: Angular→React Migration with RAE Insights         │
└─────────────────────────────────────────────────────────────┘

STEP 1: Feniks Analysis
─────────────────────────
   Feniks analyzes Angular codebase
   ├─→ Detects: AngularJS 1.5 components
   ├─→ Complexity: High (cyclomatic complexity > 20)
   └─→ Recommendation: Migrate to React

STEP 2: Query RAE for Historical Data
──────────────────────────────────────
   EnhancedRAEClient.get_historical_refactorings(
       refactor_type="angular_to_react",
       project_tags=["spa", "enterprise"],
       limit=50
   )

   RAE Returns:
   ├─→ 15 past Angular→React migrations
   ├─→ Success rate: 80% (12/15 successful)
   ├─→ Common pitfalls:
   │   • State management complexity
   │   • Routing integration issues
   │   • Component lifecycle mapping
   └─→ Successful patterns:
       • Extract state logic first
       • Incremental migration (hybrid approach)
       • Comprehensive E2E tests

STEP 3: Enrich Feniks Recommendation
──────────────────────────────────────
   EnhancedRAEClient.enrich_reflection(
       local_reflection=feniks_recommendation,
       context={"tech_stack": ["angular", "typescript"]}
   )

   Enhanced Recommendation:
   ├─→ Original: "Migrate Angular components to React"
   ├─→ + RAE Insight: "Use incremental approach (80% success)"
   ├─→ + RAE Insight: "Extract state management first (reduces risk)"
   ├─→ + RAE Warning: "Watch for routing pitfalls (failed in 3/15 projects)"
   └─→ Confidence: 0.75 → 0.90 (boosted by historical data)

STEP 4: Execute Migration (Feniks)
───────────────────────────────────
   Feniks RefactorEngine applies migration
   ├─→ Recipe: AngularToReactMigration
   ├─→ Strategy: Incremental (based on RAE insights)
   └─→ Tests: Run Behavior Guard

STEP 5: Store Outcome (Feedback Loop)
──────────────────────────────────────
   EnhancedRAEClient.store_refactor_outcome(
       refactor_decision=migration_decision,
       outcome={
           "status": "success",
           "test_results": {"passed": 48, "failed": 2},
           "metrics": {"complexity_reduction": 35},
           "lessons": ["State extraction was key", "E2E tests caught 2 regressions"]
       }
   )

   RAE Learning:
   ├─→ Updates semantic memory: "Angular→React: 13/16 success (81%)"
   ├─→ Strengthens pattern: "Extract state first"
   └─→ Meta-reflection: "System improving at Angular migrations (+5%)"
```

### Use Case 2: Self-Improving Code Quality Rules

**Scenario**: Feniks learns which complexity thresholds actually matter.

```
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOW: Learning Optimal Complexity Thresholds            │
└─────────────────────────────────────────────────────────────┘

INITIAL STATE: Feniks uses static threshold (complexity > 15)
───────────────────────────────────────────────────────────────

PROJECT 1: E-commerce (50k LOC)
─────────────────────────────────
   Feniks flags 50 functions (complexity > 15)
   Developer refactors 10 (20% acceptance)

   → Store to RAE episodic:
     "Project: ecommerce, threshold: 15, acceptance: 20%"

PROJECT 2: Banking (100k LOC)
──────────────────────────────
   Feniks flags 100 functions (complexity > 15)
   Developer refactors 5 (5% acceptance)

   → Store to RAE episodic:
     "Project: banking, threshold: 15, acceptance: 5%"

PROJECT 3: Startup MVP (10k LOC)
─────────────────────────────────
   Feniks flags 15 functions (complexity > 15)
   Developer refactors 12 (80% acceptance)

   → Store to RAE episodic:
     "Project: startup, threshold: 15, acceptance: 80%"

RAE REFLECTION ENGINE ANALYZES PATTERN:
────────────────────────────────────────
   Across 3 projects:
   ├─→ Average acceptance: 35%
   ├─→ Insight: Project size correlates with false positives
   └─→ Learning: Adjust threshold by project size
       • Small projects (<20k LOC): threshold=12 (high acceptance)
       • Medium projects (20-80k LOC): threshold=15 (balanced)
       • Large projects (>80k LOC): threshold=20 (reduce noise)

FENIKS QUERIES RAE FOR ADAPTIVE THRESHOLD:
───────────────────────────────────────────
   EnhancedRAEClient.get_refactor_recommendation(
       refactor_type="reduce_complexity",
       code_context={"project_size": 75000},
       project_context={"domain": "fintech"}
   )

   RAE Returns:
   ├─→ Recommended threshold: 18 (adjusted for large project)
   ├─→ Confidence: 0.85 (based on 3 similar projects)
   ├─→ Rationale: "Large projects have natural complexity"
   └─→ Success prediction: 45% acceptance rate

FENIKS APPLIES LEARNED THRESHOLD:
──────────────────────────────────
   Instead of flagging 100 functions (threshold=15)
   Flags 40 functions (threshold=18)
   Developer refactors 18 (45% acceptance) ✅

   → Exactly as RAE predicted!

CONTINUOUS LEARNING LOOP:
──────────────────────────
   Store new outcome to RAE
   → RAE refines model (now 4 data points)
   → Next project gets even better recommendations
```

---

## 🚀 Część 5: Migration Path

### Phase 1: Foundation (Week 1-2)

**Goal**: Bidirectional communication established

**Tasks**:
1. ✅ Implement `EnhancedRAEClient` with read operations
2. ✅ Add RAE endpoints for refactoring history
3. ✅ Basic reflection enrichment (simple query)
4. ✅ Unit tests for new client methods

**Deliverables**:
- Working bidirectional RAE client
- API endpoint: `/v2/memories/refactorings/history`
- API endpoint: `/v2/memories/patterns/search`
- Test coverage: 80%+

### Phase 2: Intelligence (Week 3-4)

**Goal**: Smart routing and cross-project learning

**Tasks**:
1. Implement `FeniksMemoryRouter`
2. Cross-project pattern detection in RAE
3. Reflection enrichment with confidence scoring
4. Dashboard for visualizing cross-project insights

**Deliverables**:
- Memory router with decision logic
- Cross-project pattern API
- Enhanced meta-reflection with RAE insights
- Grafana dashboard showing learning trends

### Phase 3: Full Synergy (Week 5-6)

**Goal**: Complete learning loop and optimization

**Tasks**:
1. Feedback loop (outcome storage → RAE learning)
2. Adaptive thresholds based on historical data
3. Longitudinal analysis (system improvement over time)
4. Performance optimization (caching, batching)

**Deliverables**:
- Complete feedback loop
- Self-improving quality rules
- Longitudinal analytics
- Performance: <200ms for enrichment

---

## 📊 Success Metrics

### Technical Metrics

| Metric | Baseline | Target (3 months) |
|--------|----------|-------------------|
| **Refactor acceptance rate** | 35% | 60% |
| **Cross-project pattern reuse** | 0% | 40% |
| **Reflection enrichment time** | N/A | <200ms |
| **RAE query success rate** | N/A | 99%+ |
| **False positive reduction** | 0% | 30% |

### Business Metrics

| Metric | Impact |
|--------|--------|
| **Developer time saved** | 20% reduction in manual code review |
| **Code quality improvement** | 15% reduction in post-refactor bugs |
| **Knowledge retention** | 100% of refactor decisions persisted |
| **Onboarding speed** | 40% faster for new projects (via patterns) |

---

## 🔗 References

### RAE Documentation
- [RAE Architecture](../concepts/architecture.md)
- [Reflection Engine V2](../REFLECTIVE_MEMORY_V1.md)
- [GraphRAG Implementation](../concepts/)
- [Multi-Model LLM](../RAE–Multi-Model_LLM-Integration-Guide.md)

### Feniks Documentation
See counterpart document: `feniks/docs/RAE_INTEGRATION_BLUEPRINT.md`

---

## 📝 Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-29 | Initial blueprint created |

---

## 👥 Contributors

- RAE Team
- Feniks Team
- Architecture designed with Claude Code

---

**Next Steps**: Implementacja Phase 1 → Create pull requests in both repositories

