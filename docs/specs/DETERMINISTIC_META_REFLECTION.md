# System 92.0: Deterministic Meta-Reflection & Swarm Synergy

## 1. Vision & Philosophy
RAE is not a chatbot with files. It is an **Operating System for Intelligence**.
System 92.0 introduces **Deterministic Meta-Reflection**: a closed-loop architecture where RAE-Feniks acts as the "Subconscious" or "Meta-Observer" for RAE-Hive, transforming episodic execution logs into rigorous, agnostic, and auditable behavioral wisdom.

**Core Tenets:**
1.  **Agnosticism:** The system observes *patterns of behavior* (loops, dead ends, success velocities), not just specific language syntax. It works for Python, C++, or Industrial Logs.
2.  **Determinism:** Meta-knowledge is served via **Silicon Oracle (System 87.0)**. Given the same memory state, the "advice" injected into an agent is mathematically identical every time.
3.  **Auditability:** Every Meta-Reflection MUST have a `provenance` chain linking it back to specific `episodic` memory UUIDs. "Why did RAE suggest this?" -> "Because of these 5 past events."

## 2. Architecture: The Synergy Loop

### A. RAE-Hive ( The Body / Execution )
*   **Role:** Executes tasks, modifies code, runs tests.
*   **Output:** Generates high-volume `episodic` logs (actions, tool outputs, errors).
*   **Constraint:** Bounded context. Cannot "remember" everything linearly.

### B. RAE-Feniks ( The Mind / Meta-Observer )
*   **Role:** Analyzes the `episodic` trace of the Hive.
*   **Mechanism:** `SwarmObserver` module.
*   **Algorithm:**
    *   Detects **Anti-Patterns** (e.g., `DECISION_LOOP`, `VALIDATION_GAP`).
    *   Detects **Success-Patterns** (e.g., `TEST_FIRST_VELOCITY`).
*   **Output:** Writes to RAE `reflective` layer with strict schema.

### C. The Feedback Loop (Context Injection)
*   **Trigger:** Orchestrator starts a new plan.
*   **Action:** RAE performs a `provenance-aware search` in the `reflective` layer.
*   **Injection:** Relevant Meta-Reflections are injected into the Orchestrator's system prompt as **Hard Constraints** or **Heuristics**.

## 3. Implementation Plan (Agentic Design Patterns)

### Phase 1: The Observer (Feniks)
*   **Pattern:** *Meta-Reflection (Gulli Ch. 4)* & *Self-Model (Gulli Ch. 11)*.
*   **Task:** Implement `SwarmObserver` in Feniks.
*   **Input:** RAE-Hive Project ID.
*   **Logic:**
    *   Map `episodic` events to a `BehaviorGraph`.
    *   Identify cycles and stalled edges.

### Phase 2: The Contract (RAE Core)
*   **Pattern:** *Auditability / Provenance*.
*   **Task:** Enforce schema in `ReflectiveLayer`.
*   **Field:** `parent_trace_ids` (List[UUID]) is MANDATORY for all meta-reflections.
*   **Validation:** Reject any reflection without grounded facts.

### Phase 3: The Injection (Hive Orchestrator)
*   **Pattern:** *Planning with Adaptability (Gulli Ch. 6)*.
*   **Task:** Modify `planner.py` / `Orchestrator` prompt.
*   **Logic:**
    *   BEFORE `plan()`: Query `reflective` layer for `project_id`.
    *   IF `reflection` found: Append to `system_instructions`.

## 4. Success Metrics
*   **Reduction in Loops:** Hive does not repeat the same error twice across sessions.
*   **Determinism:** Re-running a task sequence yields the same Meta-Reflections.
*   **Traceability:** Every "Idea" in RAE can be clicked to reveal the "Events" that created it.
