# 🛡️ RAE Governance & Compliance Framework
> **Standards Compliance:** ISO/IEC 27001 (Information Security), ISO/IEC 42001 (AI Management)

This document defines the mandatory audit trail for all AI operations within the RAE ecosystem. To maintain certification, every interaction must answer four core questions.

---

## 🧭 The Core Audit Quadrant

### 1. IDENTITY: "Who performed the action?"
- **Mechanism:** `X-Tenant-Id` + `source_agent`.
- **Constraint:** RAE rejects any interaction without a verified Tenant ID.
- **Traceability:** Every memory is cryptographically linked to the sending service/agent.

### 2. INTENT: "Why was this action taken?"
- **Mechanism:** `human_label` (Mandatory/Auto-generated).
- **Intelligent Bridge:** If an agent fails to provide a rationale, the RAE Bridge analyzes the payload to generate a readable `human_label` (e.g., *"Database Schema Optimization"*).
- **ISO 42001 Requirement:** Ensures human oversight can understand AI decisions without reading raw JSON logs.

### 3. ACTION: "What exactly was changed?"
- **Mechanism:** `Implicit Capture` (Episodic Layer).
- **Storage:** The entire `payload` is stored as an immutable event. 
- **Integrity:** RAE uses content hashing to detect any tampering with historical records.

### 4. OUTCOME: "What was the result and impact?"
- **Mechanism:** `Enterprise Guard` Metrics.
- **Parameters:**
    - `status`: (success/failed) – Did the change work?
    - `impact`: (low/high) – How critical was this operation?
    - `mem_delta_mb`: Resource footprint of the decision.
    - `duration_s`: Efficiency of the AI reasoning process.

---

## 🌉 Integration Paths

### A. For External Apps (Bridge API)
All systems MUST use the `/v2/bridge/interact` endpoint. 
**Pro-active Audit:** The Bridge will automatically assign the correct `project` (e.g., `dreamsoft_modernization`) based on semantic analysis of your data.

### B. For AI Agents (MCP)
Agents use the `save_memory` tool. RAE enforces the same Bridge logic, ensuring that even autonomous LLM thoughts are captured with proper labels and project context.

### C. For Python Core (Enterprise Guard)
Critical internal functions are wrapped in:
```python
@audited_operation(operation_name="component_migration", impact_level="high")
```
This ensures **100% automated compliance reporting** without manual logging.

---

## 📊 Auditing Tools
- **Swagger UI:** `http://localhost:8001/docs` (Interactive testing)
- **ReDoc:** `http://localhost:8001/redoc` (Clean compliance reading)
- **RAE Dashboard:** Real-time visualization of agentic patterns and audit logs.

---
*© 2026 RAE Project - Governance Division. Managed by RAE-Feniks.*
