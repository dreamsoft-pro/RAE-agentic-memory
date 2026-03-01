# 🎯 Next Session Plan: Dreamsoft Pro 2.0 (Phase 2.5 & 3)

## 📌 Status Check
- **Phase 2 (Standard)**: 100% Completed (~259 files modernized).
- **Phase 2 (Giants)**: 100% Atomic Slicing Completed (All chunks for Calc, Cart, etc., are on Node 1).
- **Architecture**: v3.3 Iron Protocol officially adopted.
- **Infrastructure**: RAE API Gateway fixed, OTel Telemetry ready, Supervisor v2 active.

---

## 🛠️ Task 1: Complete Phase 2.5 (The Semantic Glue)
**Goal**: Transform raw chunks into an exhaustive assembly manual.

1.  **Exhaustive Symbol Recovery**:
    *   Run the `SymbolExtractor` agent on all 18 giants.
    *   Generate full `symbols.json` maps (Scope, DI, Functions).
2.  **Total Contract Mapping**:
    *   Refine `contract.json` for `CalcCtrl` and `calc.html`.
    *   **Crucial**: Force the model to map **every single chunk** (0-152) to a specific component group.
    *   Generate contracts for remaining giants (`CartWidgetService`, `ConfigureProjectCtrl`, `routes`).

## 🏗️ Task 2: Launch Phase 3 (The Assembly)
**Goal**: Assemble the "LEGO bricks" into functional React modules.

1.  **Global State Infrastructure**:
    *   Implement `CalculatorContext.tsx` and `CartContext.tsx` based on recovered `symbols.json`.
    *   Bridge the new `PriceEngine.ts` with the React state.
2.  **Component Stitching**:
    *   Use the `Stitcher` agent to combine chunks into high-level components (e.g., `CalculatorForm.tsx`, `SummaryPanel.tsx`).
    *   Replace legacy `$scope` references with `useContext` or `props`.
3.  **Routing & Layout Integration**:
    *   Activate the zmodernized `routes.tsx` in the Next.js App Router.
    *   Build the main `RootLayout.tsx` with Tailwind CSS.

## 🛡️ Task 3: Behavioral Verification (Legacy Guard)
**Goal**: Prove that the new code works exactly like the 15-year-old original.

1.  **Evidence Comparison**:
    *   Compare the output of `PriceEngine.ts` with recorded values from the legacy system.
2.  **Headless Flow Test**:
    *   Run Playwright tests on the new `CalculatorView` to ensure UI interactions trigger correct state changes.

---

## 🚀 Ready for Execution (Commands for Next Session)
- **To resume work on Node 1**: `python3 agent_hive/hive_engine.py --mode contract`
- **To verify files**: `ls -R /mnt/extra_storage/RAE-agentic-memory-agnostic-core/agent_hive/work_dir/components/`
- **To monitor logic**: Check Jaeger at `http://100.68.166.117:16686`

---
**Senior Mandate**: "Do not start Phase 3 until all 18 giants have 100% complete contracts. Quality over speed."
