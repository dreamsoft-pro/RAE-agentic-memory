# RAE Usage Mandate

## Importance
The **Reasoning Agent Engine (RAE)** is the central source of truth for the ScreenWatcher project. Its usage is **CRITICAL** for:
1.  **Prevention of Context Drift:** Ensuring decisions made in previous sessions are preserved.
2.  **Quality Assurance:** Maintaining architectural consistency across iterations.
3.  **Token Efficiency:** Reducing the need to re-read files by leveraging RAE as a semantic cache.

## Protocol
- **RAE-First Priority:** Connectivity to RAE is the top priority. If the connection is lost, the agent MUST immediately attempt to restore it before proceeding with other tasks.
- **Every Session Start:** The agent MUST sync with RAE (episodic layer, tag: `session_start`).
- **Key Decisions:** Every major architectural decision or feature completion MUST be logged in RAE.
- **Doubt Resolution:** If context is missing, the agent SHOULD query RAE before asking the user or making broad assumptions.

## Connectivity
- **RAE Address:** `http://100.66.252.117:8000` (Tailscale).
- **Tenant ID:** `screenwatcher`.
- **Method:** Always use a reliable method (like a Python bridge script) to avoid shell escaping issues during API calls.
