# apps/memory-api/logging_config.py
"""
Enterprise-grade logging configuration for RAE Memory API.

This module implements sophisticated logging with:
- Structured logging via structlog
- Configurable log levels for different components
- Separation between application logs and library logs
- JSON output for production parsing
- Clean, readable output for development

Operational Excellence:
- Library logs (uvicorn, asyncpg, httpx) can be set to WARNING to reduce noise
- Application logs maintain INFO level for visibility
- All levels are configurable via environment variables
"""
import logging
import sys
import structlog
from structlog.types import Processor


def setup_logging():
    """
    Set up enterprise-grade structured logging for the application.

    Configures different log levels for:
    - External libraries (uvicorn, asyncpg, httpx, celery) - controlled by LOG_LEVEL
    - RAE application code - controlled by RAE_APP_LOG_LEVEL

    This separation ensures production logs are clean while maintaining
    visibility into application behavior.
    """
    # Import settings here to avoid circular imports
    from apps.memory_api.config import settings

    # Parse log levels from configuration
    external_log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.WARNING)
    app_log_level = getattr(logging, settings.RAE_APP_LOG_LEVEL.upper(), logging.INFO)

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run after all processors from structlog.configure()
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Configure root logger with external library level
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(external_log_level)

    # Configure application loggers with app-specific level
    app_logger = logging.getLogger("apps.memory_api")
    app_logger.setLevel(app_log_level)

    # Configure external library loggers explicitly
    # These libraries can be noisy on INFO level in production
    external_loggers = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "asyncpg",
        "httpx",
        "httpcore",
        "celery",
        "celery.worker",
        "kombu",
        "amqp"
    ]

    for logger_name in external_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(external_log_level)

    # Disable uvicorn's access log completely (we have our own middleware)
    logging.getLogger("uvicorn.access").disabled = True

    # Log the configuration for visibility
    structlog.get_logger(__name__).info(
        "logging_configured",
        external_log_level=settings.LOG_LEVEL,
        app_log_level=settings.RAE_APP_LOG_LEVEL
    )
