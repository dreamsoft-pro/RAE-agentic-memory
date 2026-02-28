# RAE-Core Architecture

## System Overview
RAE (Robotic Agent Emulation) Core acts as the centralized "Black Box" memory and intelligence gateway for the entire agentic ecosystem.

## Key Components
1. **Memory API v2**: High-performance FastAPI interface with strict multi-tenancy.
2. **Reflective Layer (The Gateway)**: 
   - **Mechanism**: Captures agentic prompts and automatically routes them to configured LLM providers (Gemini, Claude, GPT).
   - **Response Pattern**: Instead of just storing, the POST method returns the generated `message` from the LLM, effectively acting as an intelligent proxy.
3. **Storage Adapters**: 
   - **PostgreSQL**: Stores raw content and JSONB metadata.
   - **Qdrant**: Handles vector embeddings for semantic search.

## Critical Protocols
- **System 92.0 (Anti-Echo)**: Prevents infinite agentic loops by sanitizing tags and tracking lineage.
- **Fail-Fast Validation**: Database integrity check on every startup.
