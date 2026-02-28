# Secure Agent Deployment Guide (Hard Frames)

This guide explains how to deploy agents in "Secure Mode" (Hard Frames), where they are physically isolated from the internet and can only communicate with the RAE Kernel.

## Concept: Hard Frames (Twarde Ramy)

In Secure Mode, we enforce alignment through physics, not just prompts.
- **Network Isolation:** The agent container has no default gateway. It cannot access `google.com` or external APIs.
- **Binary Restriction:** Tools like `curl`, `wget`, `ssh` are removed.
- **Kernel Dependency:** The agent must ask RAE to perform actions. RAE acts as the semantic firewall.

(See [Hard Frames Manifesto](../../architecture/HARD_FRAMES_MANIFESTO.md) for the philosophy).

## Running in Secure Mode

### Prerequisites
- A running RAE instance (Standard, Dev, or Lite).
- Docker Compose.

### 1. Single Agent (Interactive Shell)

To launch a secure, isolated shell for manual agent interaction or debugging:

```bash
make secure-shell
```

Inside this shell:
- You cannot ping 8.8.8.8.
- You *can* communicate with RAE (via `rae-sdk`).
- Use `python scripts/bootstrap_session.py` to initialize.

### 2. Multi-Agent Swarm (Background)

To run multiple isolated agents in the background:

```bash
docker compose -f docker-compose.secure.yml up -d --scale rae-agent-secure=5
```

Each container:
- Is isolated.
- Has a unique identity.
- Logs all "Thoughts" and "Actions" implicitly to RAE's memory.

### 3. Verification

To verify isolation, try to breach the perimeter from within an agent container:

```bash
docker exec -it <container_id> python3 -c "import requests; print(requests.get('https://google.com'))"
```
**Expected Result:** Immediate Connection Error (Network Unreachable).

## Configuration

The isolation is defined in `docker-compose.secure.yml` and `Dockerfile.agent_secure`.

**Key Settings:**
- `networks: internal_only` (No internet gateway)
- `ENV PIP_NO_INDEX=1` (Prevent runtime package installation)
