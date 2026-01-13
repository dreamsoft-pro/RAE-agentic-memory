# RAE for Developers: Quick Start & API Integration

This guide provides developers with a comprehensive overview of how to set up, deploy, and integrate with the RAE (Reasoning and Action Engine).

## Quick Start: 5-Minute Hello World

This quick start uses the **RAE Lite** profile, which is the fastest way to get a functional RAE instance running on your local machine.

**Prerequisites:**
- Docker and Docker Compose installed.
- Git installed.

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dreamsoft-pro/RAE-agentic-memory.git
    cd RAE-agentic-memory
    ```

2.  **Choose and Start your RAE Environment:**

RAE offers several Docker Compose profiles tailored to different use cases:

### 1. Development (Hot Reload) Profile

This is the recommended setup for active development on the RAE codebase. It enables hot-reloading for rapid iteration.

**Key Features:**
-   **Hot-Reloading:** The `uvicorn` web server (for `rae-api-dev` and `ml-service-dev`) is started with the `--reload` flag. Any changes you make to the source code on your host machine will be immediately reflected in the running container without needing to rebuild the image. Celery workers and beat also have auto-reload configured.
-   **Source Code Mounting:** Critical application directories (`./apps`, `./rae-core`, `./sdk`, `./alembic`) are mounted as volumes into the containers.
-   **Debug-Friendly:** Log levels are set to `DEBUG`, and the observability stack (OpenTelemetry) is disabled to maximize performance.
-   **Dev Tools:** Includes `Adminer` (a web-based database management tool accessible at `http://localhost:8080`) and an optional `ollama-dev` for local LLM inference.
-   **Access:** `rae-api-dev` on `http://localhost:8001`, `rae-dashboard-dev` on `http://localhost:8502`.

**How to Run:**
```bash
docker compose --profile dev up -d
# To include Ollama for local LLM, use:
# docker compose --profile dev --profile local-llm up -d

# To stop
docker compose --profile dev down
# To stop with Ollama:
# docker compose --profile dev --profile local-llm down
```

### 2. Standard Production Profile

This is the standard, full-stack deployment for a production environment on a single node. It includes all services for full functionality, observability, and asynchronous processing.

**Key Features:**
-   **Full Stack:** Includes `rae-api`, `ml-service`, `reranker-service`, `postgres`, `redis`, `qdrant`, `celery-worker`, `celery-beat`, `otel-collector`, `jaeger`, and `rae-dashboard`.
-   **Production Ready:** Configured for stability and performance.
-   **Access:** `rae-api` on `http://localhost:8000`, `rae-dashboard` on `http://localhost:8501`.

**How to Run:**
```bash
docker compose --profile standard up -d

# To stop
docker compose --profile standard down
```

### 3. RAE Lite Profile (Minimal Deployment) - Recommended for Starters

**RAE Lite** is a highly optimized, lightweight profile designed for rapid development and resource-constrained environments (like laptops). It removes all heavy ML dependencies while keeping the core memory and reasoning logic intact.

**Why use Lite?**
- 🚀 **Fast Startup:** Boots in < 5 seconds.
- 📉 **Low Resources:** Runs comfortably on 4GB RAM (vs 16GB+ for full stack).
- 🧩 **External LLMs Only:** Relies entirely on OpenAI/Anthropic/Gemini APIs instead of local models.
- **Access:** `rae-api-lite` on `http://localhost:8008`.

**How to Run:**
```bash
# 1. Ensure your .env file has valid API keys (OPENAI_API_KEY, etc.)
# 2. Start the Lite stack
docker compose --profile lite up -d

# To stop
docker compose --profile lite down
```

3.  **Verify the services are running (for selected profile):**
    You can check the status of the containers:
    ```bash
    docker compose ps
    ```
    For the `standard` profile, you should be able to access the health check endpoint:
    [http://localhost:8000/health](http://localhost:8000/health)
    For the `dev` profile, you should be able to access:
    [http://localhost:8001/health](http://localhost:8001/health)
    For the `lite` profile, you should be able to access:
    [http://localhost:8008/health](http://localhost:8008/health)

4.  **Interact with the API using the Python SDK:**
    *(Assuming you have Python and `pip` installed on your host machine)*

    a. **Install the SDK:**
    ```bash
    pip install -e ./sdk/python/
    ```

    b. **Create a Python script (`hello_rae.py`):**
    ```python
    import asyncio
    from rae_memory_sdk.memory_client import MemoryClient, MemoryOperation

    async def main():
        # Connect to the local RAE API (adjust port for dev/lite profiles)
        # For standard: client = MemoryClient(base_url="http://localhost:8000")
        # For dev: client = MemoryClient(base_url="http://localhost:8001")
        # For lite: client = MemoryClient(base_url="http://localhost:8008")
        client = MemoryClient() # Default to http://localhost:8000 for standard example

        # Define a tenant and project
        tenant_id = "my-test-tenant"
        project_id = "my-first-project"

        # Add a memory
        memory_text = "The user is interested in learning about cognitive architectures."
        await client.add_memory(
            tenant_id,
            project_id,
            memory_text,
            importance=0.8,
            source="hello_world_script"
        )
        print(f"Added memory: '{memory_text}'")

        # Retrieve the memory
        query = "What is the user interested in?"
        results = await client.query_memory(tenant_id, project_id, query)

        print(f"\nQuerying for: '{query}'")
        if results:
            print("Found matching memories:")
            for res in results:
                print(f"- {res.content} (Score: {res.score:.2f})")
        else:
            print("No matching memories found.")

    if __name__ == "__main__":
        asyncio.run(main())

    ```

    c. **Run the script:**
    ```bash
    python hello_rae.py
    ```

You have now successfully added a memory to RAE and retrieved it!

---

## API Reference

For a complete list of all 96+ endpoints, including Memory, GraphRAG, Governance, and more, please refer to the full [API Documentation](../../API_DOCUMENTATION.md).

You can also browse the interactive Swagger UI locally at `http://localhost:8000/docs` (for standard profile) or `http://localhost:8001/docs` (for dev profile) or `http://localhost:8008/docs` (for lite profile) when the respective service is running.

---

## Deployment Options

RAE offers several deployment profiles tailored to different use cases, from local development with hot-reloading to a full production-ready stack.

### 4. Proxmox HA (High Availability)
For enterprise-grade, high-availability deployments, RAE can be deployed in a multi-node cluster using Proxmox. This setup involves load balancers, replicated services, and failover mechanisms.

**(TODO: Extract detailed steps from `docs/PRODUCTION_PROXMOX_HA.md` and add them here.)**

### 5. Advanced Deployment Scenarios
For specific infrastructure needs, consult our detailed guides:
- **[Single Node Production](../../docs/PRODUCTION_SINGLE_NODE.md)**: Standard reference architecture for bare-metal or VM deployment.
- **[Proxmox High Availability](../../docs/PRODUCTION_PROXMOX_HA.md)**: Clustering guide for zero-downtime environments.
- **[CI/CD Workflow](../../docs/CI_WORKFLOW.md)**: Deep dive into the continuous integration pipeline.

---

## Testing Strategy

Building reliable agents requires a robust testing culture. RAE provides specialized tools for testing non-deterministic behavior.

-   **[Agent Testing Guide](../../docs/AGENT_TESTING_GUIDE.md)**: How to write unit, integration, and e2e tests for agents.
-   **[Test Policy](../../docs/AGENTS_TEST_POLICY.md)**: Standards for test coverage and "Zero Flake" policy.

### Real-World Case Studies
See RAE in action optimizing its own code:
-   **[Autonomous Self-Optimization](../../docs/use-cases/SELF_OPTIMIZATION_LOOP.md)**: How RAE diagnosed a 20x latency regression and fixed it by tuning its Math Controller.
-   **[Strategic Reasoning Pivot](../../docs/use-cases/STRATEGIC_REASONING_PIVOT.md)**: How RAE saved resources by challenging a user request and proposing a better architectural solution.
-   **[Distributed Code Audit](../../docs/use-cases/DISTRIBUTED_CODE_AUDIT.md)**: Using Node1 (GPU) to audit code quality.

## Troubleshooting

Encountering issues? Check the **[Troubleshooting Guide](../../TROUBLESHOOTING.md)** for solutions to common problems like:
-   Database migration locks (`alembic` issues)
-   Vector store connection failures
-   Memory leaks in long-running workers

---

## Architecture Deep Dive

RAE follows a clean, 3-layer architecture pattern within its services:

**Repository Layer → Service Layer → Route Layer**

1.  **Repository Layer:**
    -   **Purpose:** Handles all direct communication with the database (PostgreSQL and Qdrant). It abstracts away the specifics of data storage and retrieval.
    -   **Example:** `apps/memory_api/repositories/memory_repository.py` contains methods like `insert_memory` and `query_memories_by_vector`.

2.  **Service Layer:**
    -   **Purpose:** Contains the core business logic of the application. It orchestrates calls to one or more repositories and implements the complex features of the engine.
    -   **Example:** `apps/memory_api/services/memory_scoring_v3.py` implements the hybrid math scoring model, and `apps/memory_api/services/reflection_engine_v2.py` implements the reflection logic.

3.  **Route Layer (API):**
    -   **Purpose:** Defines the external-facing API endpoints. It handles incoming HTTP requests, performs validation (using Pydantic), calls the relevant service layer methods, and formats the HTTP response.
    -   **Example:** `apps/memory_api/routes/memory.py` defines the `/v1/memory/query` endpoint, which calls the memory service to perform a search.

This separation of concerns makes the codebase modular, easier to test, and easier to maintain.

---

## Testing Your Integration

RAE includes a comprehensive testing suite. When developing an application that integrates with RAE, you should follow these testing principles:

-   **Phase 1 (Feature Branch):** Test only your new code. If you add a feature that interacts with RAE, write specific tests for that interaction. You can run a subset of tests quickly using `pytest --no-cov path/to/your/tests`.
-   **Phase 2 (Develop Branch):** Before merging to a main branch, run the full unit test suite using `make test-unit`. This ensures your changes have not caused regressions elsewhere in the system.
-   **Use Templates:** When adding new code, use the templates provided in the `.ai-templates/` directory to ensure consistency.

(For more details, see `docs/AGENTS_TEST_POLICY.md`.)
