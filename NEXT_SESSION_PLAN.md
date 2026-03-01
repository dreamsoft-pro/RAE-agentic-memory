# Next Session Plan: Repository Cleanup & Standardization

## Objective
The root directory of the RAE repository is currently cluttered with operational scripts, backups, and temporary files. The goal is to establish a senior-grade project structure that adheres to the **Model Economy** and **Zero Drift** principles.

## 🧹 Phase 1: Structural Cleanup (Muda Elimination)
- [ ] **Move Scripts**: Migrate all top-level `.py` scripts (e.g., `verify_hard_frames_v2.py`, `business_continuity_indexer.py`) to the `scripts/` directory.
- [ ] **Archive Legacy**: Move old guide files and backups (e.g., `SILICON_ORACLE_100K_GUIDE.md`, `PLAN_RECOVERY_LUMINA.md`) to a new `docs/archive/` directory.
- [ ] **Unified Config**: Move all root-level configuration files to the `config/` directory.
- [ ] **Remove Junk**: Identify and delete temporary log files (`*.log`), pid files, and unused `.sh` files from the root.

## 🏗️ Phase 2: Factory Reactivation (Operacja Lustro)
- [ ] **Verify Node 1 Status**: Check if Kubuś has finished and if Lumina is ready for production.
- [ ] **Sync Contracts**: Propagate the **Global Contract Atlas v1.5** to Node 1.
- [ ] **Restart Swarm**: Re-launch the **Consensus Swarm Engine** using the newly established Hard Frames 2.1 protocols.
- [ ] **Audit First 10**: Perform a manual senior-level audit of the first 10 components generated under the new rygor.

## ⚖️ Phase 3: Senior Architecture Standard
- [ ] **Zod Schema Injection**: Update the Hive Engine to automatically generate Zod schemas based on the MySQL dump.
- [ ] **Tailwind Token Validator**: Add a linter rule to L2 Structural validation that checks for Tailwind utility classes instead of CSS variables.

---
**Status:** System is stable, unified, and auditable. Ready for deep refactoring.
**Last Action:** Pushed v3.6.1-LTS documentation and error protocol to GitHub.
