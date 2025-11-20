# Configuration Management

The RAE Agentic Memory system is configured primarily through environment variables. For local development, these can be conveniently placed in a `.env` file at the root of the project.

## Loading Order

The configuration is managed by the `pydantic-settings` library, which loads settings from the following sources in order:

1.  Arguments passed to the settings object constructor (programmatic).
2.  Environment variables.
3.  Variables defined in the `.env` file.

This means that an environment variable will always take precedence over a value in the `.env` file.

## Key Configuration Variables

Below are the most important configuration variables for running RAE.

### Database Settings

-   `POSTGRES_HOST`: The hostname of the PostgreSQL database. Defaults to `localhost`. In Docker, this should be the name of the service (e.g., `postgres`).
-   `POSTGRES_PORT`: The port of the PostgreSQL database. Defaults to `5432`.
-   `POSTGRES_USER`: The username for the PostgreSQL database.
-   `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
-   `POSTGRES_DB`: The name of the PostgreSQL database.

### Vector Store Settings

-   `VECTOR_STORE_BACKEND`: The vector store to use. Can be `qdrant` or `pgvector`. Defaults to `qdrant`.
-   `QDRANT_HOST`: The hostname of the Qdrant vector store. Defaults to `localhost`. In Docker, this is `qdrant`.
-   `QDRANT_PORT`: The port for the Qdrant vector store. Defaults to `6333`.

### Cache Settings

-   `REDIS_HOST`: The hostname of the Redis server. Defaults to `localhost`. In Docker, this is `redis`.
-   `REDIS_PORT`: The port for the Redis server. Defaults to `6379`.
-   `REDIS_DB`: The Redis database to use for the cache. Defaults to `0`.

### LLM Backend Settings

-   `RAE_LLM_BACKEND`: The LLM provider to use. Supported values are `gemini`, `openai`, `ollama`, and `anthropic`.
-   `RAE_LLM_MODEL_DEFAULT`: The default model to use for the selected backend (e.g., `gpt-4o-mini` for OpenAI, `llama3` for Ollama).
-   `RAE_LLM_MAX_RETRIES`: How many times to retry a failed LLM call. Defaults to `3`.
-   `OPENAI_API_KEY`: Your API key for OpenAI.
-   `ANTHROPIC_API_KEY`: Your API key for Anthropic.
-   `OLLAMA_API_URL`: The URL for your Ollama instance (e.g., `http://localhost:11434`).

### Security Settings

-   `OAUTH_ENABLED`: A boolean to enable or disable OAuth2 authentication. Defaults to `True`. When disabled, authentication is bypassed (for local development or testing only).
-   `OAUTH_DOMAIN`: The domain of your OAuth2 provider (e.g., `your-tenant.us.auth0.com`). This is used to fetch the public keys for token verification.
-   `OAUTH_AUDIENCE`: The "audience" claim for the JWT, which is typically the unique identifier of your API (e.g., `https://my-rae-api.com`).
-   `TENANCY_ENABLED`: Whether to enforce multi-tenancy. When `True`, the `X-Tenant-Id` header is required for all requests. Defaults to `True`.
-   `ALLOWED_ORIGINS`: A comma-separated list of allowed origins for CORS (e.g., `http://localhost:3000,https://my-app.com`).

### Memory Lifecycle Settings

-   `MEMORY_RETENTION_DAYS`: The number of days to keep `episodic` memories before they are automatically pruned. Set to `0` or a negative number to disable pruning. Defaults to `30`.

## Example `.env` File

```env
# --- DATABASE ---
POSTGRES_HOST=postgres
# ... (rest of DB settings)

# --- LLM ---
RAE_LLM_BACKEND=openai
RAE_LLM_MODEL_DEFAULT=gpt-4o-mini
OPENAI_API_KEY="your-openai-api-key"

# --- SECURITY ---
OAUTH_ENABLED=True
OAUTH_DOMAIN="your-tenant.us.auth0.com"
OAUTH_AUDIENCE="https://your-api-audience.com"
TENANCY_ENABLED=True
ALLOWED_ORIGINS="http://localhost:3000"

# --- MEMORY LIFECYCLE ---
MEMORY_RETENTION_DAYS=30
```
