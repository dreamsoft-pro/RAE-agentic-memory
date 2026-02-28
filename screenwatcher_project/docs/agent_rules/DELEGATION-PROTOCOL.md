# RAE Delegation & Compute Node Protocol

## Purpose
To maximize token efficiency, performance, and code quality by leveraging dedicated compute nodes (like **Node1 / kubus-gpu-01**) for intensive tasks such as code generation, auditing, and complex analytics.

## Node Discovery
- Compute nodes are managed by the RAE Control Plane.
- Current active nodes MUST be listed at the start of each delegation phase.
- Primary node: `kubus-gpu-01` (GPU Accelerated).

## Task Lifecycle
1.  **Preparation:** The Agent defines a clear, self-contained specification for the task.
2.  **Creation:** Task is pushed to `POST /control/tasks` with a specific `type` (e.g., `code_generation`, `audit`).
3.  **Polling:** The Agent polls `GET /control/tasks/{id}` for the result.
4.  **Verification:** The Agent verifies the output against the specification.
5.  **Reflection:** Results (success/failure, quality, time) are logged to RAE (reflective layer) to improve future prompts.

## Standards for Prompts (Delegation)
- **Context-Rich:** Include relevant file structures or snippets.
- **Strict Format:** Request specific output formats (JSON, raw code blocks).
- **Constraints:** Clearly state libraries, versions (e.g., Django 5.2), and OS (win32).

## Continuous Improvement
- **Lesson Learning:** After each task, push a memory to RAE with tag `delegation_lesson`.
- **Node Specialization:** Identify which nodes perform better at specific tasks (e.g., Node A for Python, Node B for JS).
