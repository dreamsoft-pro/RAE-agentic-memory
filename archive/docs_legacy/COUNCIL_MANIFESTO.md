# 🏛️ THE AGENTIC COUNCIL CONSTITUTION (3x3 PROTOCOL)

## 📜 CORE MANDATE
Every piece of code generated in this factory must be validated by a 3-Tiered Council structure. No single model can decide on the final output.

## 🏗️ LAYER STRUCTURE (3x3)

### 1. TIER 1: THE ECONOMY COUNCIL (Local)
- **Architect:** Qwen 2.5 14B (Code generation)
- **Inspector:** DeepSeek Coder V2 16B (Logic & Parity audit)
- **Linter:** Llama 3.1 8B (Tailwind & TS standards)
- **Rule:** Requires 2/2 audit PASS to deploy.

### 2. TIER 2: THE STANDARD COUNCIL (Hybrid)
- **Leader:** Gemini 1.5 Pro (Strategic direction)
- **Local Experts:** DeepSeek 16B & Qwen 14B (Technical verification)
- **Rule:** Triggered if Tier 1 fails 3 times.

### 3. TIER 3: THE ORACLE COUNCIL (Cloud)
- **Strategist A:** Gemini 1.5 Pro
- **Strategist B:** Claude 4.5 Opus
- **Strategist C:** GPT-4o
- **Rule:** Reserved for critical infrastructure and complex business logic.

## 🛡️ ENFORCEMENT
- All scripts are persisted on physical disk (/mnt/extra_storage) and committed to Git.
- Master Switch (`start_factory_v2.sh`) strictly deploys ONLY these versioned scripts.
