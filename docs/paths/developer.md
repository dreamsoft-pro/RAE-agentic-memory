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

2.  **Start the RAE Lite stack:**
    ```bash
    docker-compose -f docker-compose.lite.yml up -d
    ```
    This command will start the core RAE API, a PostgreSQL database, a Redis cache, and a Qdrant vector database.

3.  **Verify the services are running:**
    You can check the status of the containers:
    ```bash
    docker-compose -f docker-compose.lite.yml ps
    ```
    You should also be able to access the health check endpoint:
    [http://localhost:8000/health](http://localhost:8000/health)

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
        # Connect to the local RAE API
        client = MemoryClient()

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

You can also browse the interactive Swagger UI locally at `http://localhost:8000/docs` when the service is running.

---

## Deployment Options

RAE offers several deployment profiles tailored to different use cases, from local development with hot-reloading to a full production-ready stack.

### 1. Local Development (Hot Reload)

This is the recommended setup for active development on the RAE codebase. It uses `docker-compose.dev.yml` as an override file to enable hot-reloading.

**Key Features:**
-   **Hot-Reloading:** The `uvicorn` web server is started with the `--reload` flag. Any changes you make to the source code on your host machine will be immediately reflected in the running container without needing to rebuild the image.
-   **Source Code Mounting:** The `./apps` and `./sdk` directories are mounted as read-only volumes into the containers. This allows the reload mechanism to detect file changes.
-   **Debug-Friendly:** Log levels are set to `DEBUG`, and the observability stack (OpenTelemetry) is disabled to maximize performance.
-   **Dev Tools:** Includes `Adminer`, a web-based database management tool accessible at `http://localhost:8080`.

**How to Run:**
```bash
# Use both the base and dev override files
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# To stop
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```

### 2. RAE Lite (Minimal Deployment)

This profile is perfect for small teams, demos, or development environments where the full observability and background processing stack is not required. It's a single-server setup that is easy to manage.

**Source File:** `docker-compose.lite.yml`

**Stack:**
-   **Included:** `rae-api`, `postgres`, `redis`, `qdrant`
-   **Excluded:** `ml-service`, `celery-worker`, `celery-beat`, observability stack, dashboard.

**How it Works:**
Features are disabled via environment variables in the `rae-api` service:
```yaml
environment:
  - ML_SERVICE_ENABLED=false
  - RERANKER_ENABLED=false
  - CELERY_ENABLED=false
```

**How to Run:**
```bash
docker-compose -f docker-compose.lite.yml up -d
```

### 3. RAE Server (Standard Production)

This is the standard, full-stack deployment for a production environment on a single node. It includes all services for full functionality, observability, and asynchronous processing.

**Source File:** `docker-compose.yml`

**Full Stack:**
-   `rae-api`: The main API.
-   `ml-service`: A separate service for heavy ML models, isolating them from the main API.
-   `postgres`: The primary database with `pgvector`.
-   `redis`: Caching and Celery broker.
-   `qdrant`: Dedicated vector database.
-   `celery-worker` & `celery-beat`: For background tasks like memory consolidation and reflection.
-   `otel-collector` & `jaeger`: A full observability stack for distributed tracing.
-   `rae-dashboard`: An optional Streamlit dashboard for visualizing memory.

**How to Run:**
```bash
docker-compose -f docker-compose.yml up -d
```

### 4. Proxmox HA (High Availability)
For enterprise-grade, high-availability deployments, RAE can be deployed in a multi-node cluster using Proxmox. This setup involves load balancers, replicated services, and failover mechanisms.

**(TODO: Extract detailed steps from `docs/PRODUCTION_PROXMOX_HA.md` and add them here.)**

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

**(For more details, see `docs/AGENTS_TEST_POLICY.md`.)**