# NEXT SESSION PLAN

## 🚨 CRITICAL: CI/CD Hygiene

The project currently fails `make lint` with **420 errors**. We cannot merge to `main` until this is fixed.

1. **Auto-Fix Linter:**
   ```bash
   .venv/bin/ruff check . --fix
   .venv/bin/ruff format .
   ```
2. **Manual Linter Fixes:**
   - Address unused imports (F401).
   - Fix bare exceptions (B904).
   - Fix argument defaults (B008).
3. **Verify:**
   ```bash
   make lint
   make test-unit
   ```
4. **Push:**
   Once `make lint` is green, push to `develop`.

## Secondary Goals
- Continue increasing test coverage for `apps/memory_api/routes/dashboard.py`.
