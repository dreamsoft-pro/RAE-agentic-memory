# RAE-Core Architecture

## System Overview
RAE (Robotic Agent Emulation) Core acts as the centralized "Black Box" memory and intelligence gateway for the entire agentic ecosystem.

## Key Components
1. **Memory API v2**: High-performance FastAPI interface with strict multi-tenancy and Hard Frames 2.1 enforcement.
2. **The 6-Layer Memory Manifold**:
   - **Sensory**: Filtering and TTL-based signal capture.
   - **Episodic**: Immutable event sourcing.
   - **Working**: Isolated context for active tasks (Hard Frames).
   - **Semantic**: Knowledge Graph and deep indexing.
   - **Long-term**: Permanent institutional records.
   - **Reflective**: 3-tiered QFT-inspired intelligence core (L1 Operational, L2 Structural, L3 Meta).
3. **Reflective Engine (The Gateway)**: 
   - **Mechanism**: Captures agentic prompts and automatically routes them to configured LLM providers (Gemini, Claude, GPT).
   - **Validation**: Every decision is passed through the 3-layer contract validation pipeline before persistence.
4. **Storage Adapters**: 
   - **PostgreSQL**: Stores raw content, JSONB metadata, and Graph relationships.
   - **Qdrant**: Handles multi-vector embeddings for agnostic semantic search.

## Critical Protocols
- **System 92.0 (Anti-Echo)**: Prevents infinite agentic loops by sanitizing tags and tracking lineage.
- **Fail-Fast Validation**: Database integrity check on every startup.
