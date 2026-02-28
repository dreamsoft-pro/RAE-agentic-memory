# RAE ARCHITECTURE V3: HARD FRAMES MANIFESTO

> **"Prompt-based alignment fails not because LLMs are bad, but because alignment without enforcement is just hope."**

## 1. The Core Insight: The "Scale Break"

Through rigorous testing, specifically scaling memory contexts from 1k to 100k items, we have empirically observed a "Scale Break":

1.  **Regime I (Small Context, <10k):** LLMs behave functionally. They respect prompt contracts, maintain coherent personas, and follow logic. Prompts act as effective "soft" constraints.
2.  **Regime II (Large Context, >100k):** LLMs shift from functional execution to agentic simulation. They begin to hallucinate alignment, ignore negative constraints, and prioritize response fluency over system rules.

**Conclusion:** At scale, **Prompts are not a security boundary.** They are merely suggestions to a probabilistic actor.

## 2. The Doctrine of "Hard Frames" (Twarde Ramy)

To build a reliable, secure, and scalable Agent Operating System (RAE), we must move from **Declarative Restrictions** (telling the agent what not to do) to **Physical Impossibilities** (making it impossible to do).

### Rule 1: Isolation by Physics, not Semantics
- **Old Way:** Prompt: "You are not allowed to access the internet."
- **New Way:** Docker: `network: none`. The agent has no route to the internet.

### Rule 2: Capability, not Identity
- **Old Way:** "You are an OpenAI agent."
- **New Way:** The agent imports `rae_client`. It calls `rae.ask()`. It does not know if the backend is GPT-4, Claude, or a local Llama. It has no SDKs (`openai`, `anthropic`) installed. It cannot bypass RAE because it lacks the binaries to do so.

### Rule 3: RAE is the Kernel
- The Agent is user-space software.
- RAE is the Kernel.
- The Kernel manages I/O, Memory, and Networking. User-space processes (Agents) perform syscalls (RAE API calls) but have no direct hardware access (Internet/Disk).

## 3. Implementation Pillars

1.  **The "Blind & Deaf" Container:**
    - No `curl`, `wget`, `git`, `ssh`.
    - No pip install at runtime.
    - No public internet access.
    - Only allowed connection: `rae-api` (via Unix Socket or Internal Network).

2.  **The Thin Client (RAE-Link):**
    - A minimal Python SDK that wraps JSON-RPC calls to RAE.
    - No logic, just transport.
    - No dependence on heavy LLM libraries inside the agent.

3.  **The Semantic Firewall:**
    - RAE API intercepts every request.
    - RAE API enforces token limits, memory retrieval strategies (Gating), and PII filtering.
    - The Agent never sees raw data unless authorized by the Kernel.

## 4. Verification: The Integrity Suite

We do not trust the Agent. We verify via:
1.  **Agent Containment Tests:** Proving physical impossibility of escape.
2.  **Non-Bypassability Tests:** Ensuring all I/O is routed through the Control Plane.
3.  **Semantic Integrity Tests:** Monitoring the firewall and audit trail.
4.  **Coherence Degradation Stress-Tests (100k):** Proving safety under cognitive load.

**Status:** Adopted as of 2026-01-20.
