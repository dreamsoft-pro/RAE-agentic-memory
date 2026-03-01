# RAE & Node1 Communication Rules

## 1. Connection Details
- **RAE API (Control Node)**: `http://100.66.252.117:8000` (via Tailscale)
- **Tenant ID**: `screenwatcher`
- **Project**: `screenwatcher_project`

## 2. Valid Task Types for Node1
Use `RAETaskBridge.create_task(task_type, payload)` with the following types:

| Task Type | Purpose | Payload Requirements |
|-----------|---------|----------------------|
| `shell_command` | Execute OS commands on Node1 | `{"command": "string"}` |
| `llm_inference` | Direct model call (single response) | `{"model": "string", "prompt": "string"}` |
| `code_verify_cycle` | Code Factory loop (Generate + Audit) | `{"prompt": "string", "model_generate": "string", "model_audit": "string"}` |

## 3. Node1 Capabilities (kubus-gpu-01)
- **GPU**: NVIDIA RTX 4080 (16GB VRAM)
- **Models available**:
  - `deepseek-coder:33b` (Recommended for generation)
  - `deepseek-coder:6.7b` (Recommended for audit/speed)
  - `ollama` (Engine)

## 4. Known Issues & Solutions
- **Błąd unknown_task_type**: Wynika z używania nazw takich jak `code_factory` lub `node1`. Zawsze używaj `code_verify_cycle` dla pętli jakości.
- **Database Errors (relation "reflections" does not exist)**: Wskazuje na brakujące migracje w RAE. Należy uruchomić `alembic upgrade head` w kontenerze RAE.
- **TimeoutError**: Może oznaczać problem z Tailscale lub przeciążenie bazy danych RAE.

## 5. Implementation Workflow
1. Prepare prompt with full context (Models, Logic, Rules).
2. Dispatch via `code_verify_cycle`.
3. Wait for `COMPLETED` status.
4. Verify `is_passed: true` and extract code from `writer_output`.
