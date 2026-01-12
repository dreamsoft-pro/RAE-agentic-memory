# RAE-Lite Debugging - Next Session Plan

## Summary of Previous Session

We have successfully diagnosed and implemented fixes for several issues preventing the `rae-api-lite` service from starting:
1.  **Missing `command`**: Added an explicit `command` to `rae-api-lite` in `docker-compose.yml` to use the correct port (`8001`).
2.  **Profile Isolation**: Added `profiles: ["standard"]` to all non-lite services to ensure they do not start with the `lite` profile.
3.  **Database Creation**: Fixed the `database "rae_lite" does not exist` error by adding a `000_create_database.sql` DDL script and correcting the `postgres-lite` healthcheck to use `pg_isready`.
4.  **Telemetry Dependency**: Removed the hard dependency on OpenTelemetry in `logging_config.py` by making the import and usage conditional, fixing a critical `ImportError` in the lite profile.
5.  **UUID TypeError**: Fixed the `invalid input for query argument... (expected str, got UUID)` error by casting UUID objects to strings in `apps/memory_api/main.py`.
6.  **Missing Volume Mount**: Added the necessary volume mounts (`apps`, `rae-core`, etc.) to the `rae-api-lite` service to ensure code changes are reflected in the container.

## Current Status

Despite these fixes, the `rae-api-lite` container is still reported to be in a restart loop. This indicates a fatal crash that happens immediately upon startup, which we have been unable to capture in the Docker logs.

## Plan for Next Session

The top priority is to get direct, unbuffered feedback from the container's startup commands.

1.  **Modify `docker-compose.yml`**: Change the `command` for the `rae-api-lite` service to `["sleep", "3600"]`. This will start the container and keep it running without attempting to start the application, providing a stable environment for debugging.
2.  **Start Services**: Run `docker compose --profile lite up -d --force-recreate` after cleaning volumes (`down -v`).
3.  **Enter the Container**: Use `docker exec -it rae-api-lite bash` to get an interactive shell inside the running container.
4.  **Manual Alembic Migration**: Inside the container, run `alembic upgrade head` and observe its direct output for any errors.
5.  **Manual Application Startup**: If the migration is successful, run `uvicorn apps.memory_api.main:app --host 0.0.0.0 --port 8001` directly in the shell.
6.  **Observe Output**: The output from Uvicorn will be printed directly to the interactive terminal, bypassing any issues with Docker's logging drivers or `bash -c` buffering. This will show the exact error causing the application to crash.