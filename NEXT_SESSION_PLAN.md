# Next Session Plan: Dashboard Debugging & API v1 Cleanup

## 1. Dashboard "Zero Memories" Investigation
- **Symptom:** Dashboard connects, but stats show 0 and feed is empty.
- **Hypothesis A:** Tenant/Project ID mismatch (default vs actual data).
- **Hypothesis B:** API v2 Stats response structure mismatch in `api_client.py`.
- **Action:** Add detailed logging to `api_client.py` response parsing and debug locally.

## 2. API v1 Retirement
- **Goal:** Remove `apps/memory_api/api/v1/memory.py` and switch all consumers to v2.
- **Prerequisite:** Ensure Dashboard works 100% on v2.
- **Task:** Audit other clients (SDK, Agents) for v1 usage.

## 3. Dashboard Features Expansion
- **Timeline:** Implement Timeline visualization using Plotly/NiceGUI.
- **Graph:** Implement 3D Graph using `ag-grid` or `vis-network`.
- **Query Lab:** Add "Szubar Mode" toggle and weight sliders.

## 4. RAE-Windows Hardware Adaptation (Continued)
- [ ] Hardware Probe implementation.
- [ ] Profile Mapping logic.
- [ ] LlamaCppAdapter for local inference.

## 5. RAE-Mesh & Federation
- Verify federation endpoints with the new v2 API structure.