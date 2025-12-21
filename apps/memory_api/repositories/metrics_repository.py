"""
Metrics Repository - Time Series Data Operations

Provides storage and retrieval operations for dashboard metrics time series data.
"""

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, cast

import asyncpg
import structlog

logger = structlog.get_logger(__name__)


class MetricsRepository:
    """Repository for time series metrics operations."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def record_metric(
        self,
        tenant_id: str,
        project_id: str,
        metric_name: str,
        value: float,
        dimensions: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        timestamp: Optional[datetime] = None,
    ) -> int:
        """
        Record a single metric data point.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            metric_name: Metric name (e.g., 'memory_count', 'search_quality_mrr')
            value: Metric value
            dimensions: Optional dimensions for filtering
            tags: Optional tags
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Metric ID
        """
        async with self.pool.acquire() as conn:
            metric_id = await conn.fetchval(
                """
                SELECT record_metric($1, $2, $3, $4, $5, $6)
                """,
                tenant_id,
                project_id,
                metric_name,
                value,
                json.dumps(dimensions) if dimensions else "{}",
                tags or [],
            )

        return cast(int, metric_id)

    async def record_metrics_batch(
        self,
        tenant_id: str,
        project_id: str,
        metrics: List[Tuple[str, float, Optional[Dict], Optional[List[str]]]],
    ) -> int:
        """
        Record multiple metric data points efficiently.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            metrics: List of tuples (metric_name, value, dimensions, tags)

        Returns:
            Number of metrics recorded
        """
        async with self.pool.acquire() as conn:
            # Use COPY for bulk insert if many metrics
            if len(metrics) > 100:
                # TODO: Implement COPY-based bulk insert for better performance
                pass

            # For now, use simple batch insert
            values = []
            for metric_name, value, dimensions, tags in metrics:
                values.append(
                    (
                        tenant_id,
                        project_id,
                        metric_name,
                        value,
                        json.dumps(dimensions) if dimensions else "{}",
                        tags or [],
                        datetime.now(timezone.utc),
                    )
                )

            # Batch insert
            await conn.executemany(
                """
                INSERT INTO metrics_timeseries (
                    tenant_id, project_id, metric_name, value,
                    dimensions, tags, timestamp, metric_type
                )
                SELECT $1, $2, $3, $4, $5::jsonb, $6, $7,
                       COALESCE(
                           (SELECT metric_type FROM metric_definitions WHERE metric_name = $3),
                           'gauge'
                       )
                """,
                values,
            )

        logger.info(
            "metrics_batch_recorded",
            tenant_id=tenant_id,
            count=len(metrics),
        )

        return len(metrics)

    async def get_timeseries(
        self,
        tenant_id: str,
        project_id: str,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        aggregation_interval: Optional[str] = "1 hour",
    ) -> List[Dict[str, Any]]:
        """
        Get time series data for a metric.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            metric_name: Metric name
            start_time: Start of time range
            end_time: End of time range
            aggregation_interval: PostgreSQL interval string (e.g., '1 hour', '15 minutes', '1 day')

        Returns:
            List of data points with timestamp, value, and count
        """
        async with self.pool.acquire() as conn:
            try:
                # Try using the get_metric_timeseries function
                records = await conn.fetch(
                    """
                    SELECT * FROM get_metric_timeseries($1, $2, $3, $4, $5, $6::interval)
                    """,
                    tenant_id,
                    project_id,
                    metric_name,
                    start_time,
                    end_time,
                    aggregation_interval,
                )
            except asyncpg.exceptions.UndefinedFunctionError:
                # Fallback to manual query if function doesn't exist
                records = await conn.fetch(
                    """
                    SELECT
                        date_trunc('hour', timestamp) AS bucket_timestamp,
                        AVG(value) AS metric_value,
                        COUNT(*)::INTEGER AS data_points
                    FROM metrics_timeseries
                    WHERE tenant_id = $1
                      AND project_id = $2
                      AND metric_name = $3
                      AND timestamp BETWEEN $4 AND $5
                    GROUP BY date_trunc('hour', timestamp)
                    ORDER BY date_trunc('hour', timestamp) ASC
                    """,
                    tenant_id,
                    project_id,
                    metric_name,
                    start_time,
                    end_time,
                )

        return [dict(r) for r in records]

    async def get_latest_metric_value(
        self, tenant_id: str, project_id: str, metric_name: str
    ) -> Optional[float]:
        """
        Get the most recent value for a metric.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            metric_name: Metric name

        Returns:
            Latest metric value or None
        """
        async with self.pool.acquire() as conn:
            value = await conn.fetchval(
                """
                SELECT value
                FROM metrics_timeseries
                WHERE tenant_id = $1
                  AND project_id = $2
                  AND metric_name = $3
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                tenant_id,
                project_id,
                metric_name,
            )

        return float(value) if value is not None else None

    async def get_metric_statistics(
        self,
        tenant_id: str,
        project_id: str,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
    ) -> Dict[str, Any]:
        """
        Get statistical summary for a metric over a time range.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            metric_name: Metric name
            start_time: Start of time range
            end_time: End of time range

        Returns:
            Dictionary with min, max, avg, sum, count, stddev
        """
        async with self.pool.acquire() as conn:
            stats = await conn.fetchrow(
                """
                SELECT
                    MIN(value) AS min_value,
                    MAX(value) AS max_value,
                    AVG(value) AS avg_value,
                    SUM(value) AS sum_value,
                    COUNT(*) AS data_points,
                    STDDEV(value) AS stddev_value
                FROM metrics_timeseries
                WHERE tenant_id = $1
                  AND project_id = $2
                  AND metric_name = $3
                  AND timestamp BETWEEN $4 AND $5
                """,
                tenant_id,
                project_id,
                metric_name,
                start_time,
                end_time,
            )

        return dict(stats) if stats else {}

    async def get_available_metrics(
        self, tenant_id: Optional[str] = None, project_id: Optional[str] = None
    ) -> List[str]:
        """
        Get list of available metrics.

        Args:
            tenant_id: Optional tenant filter
            project_id: Optional project filter

        Returns:
            List of unique metric names
        """
        async with self.pool.acquire() as conn:
            if tenant_id and project_id:
                records = await conn.fetch(
                    """
                    SELECT DISTINCT metric_name
                    FROM metrics_timeseries
                    WHERE tenant_id = $1 AND project_id = $2
                    ORDER BY metric_name
                    """,
                    tenant_id,
                    project_id,
                )
            elif tenant_id:
                records = await conn.fetch(
                    """
                    SELECT DISTINCT metric_name
                    FROM metrics_timeseries
                    WHERE tenant_id = $1
                    ORDER BY metric_name
                    """,
                    tenant_id,
                )
            else:
                records = await conn.fetch(
                    """
                    SELECT DISTINCT metric_name
                    FROM metrics_timeseries
                    ORDER BY metric_name
                    """
                )

        return [r["metric_name"] for r in records]

    async def get_metric_definition(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metric definition metadata.

        Args:
            metric_name: Metric name

        Returns:
            Metric definition dict or None
        """
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                "SELECT * FROM metric_definitions WHERE metric_name = $1", metric_name
            )

        return dict(record) if record else None

    async def cleanup_old_metrics(self, retention_days: int = 365) -> int:
        """
        Delete old metrics data beyond retention period.

        Args:
            retention_days: Number of days to retain

        Returns:
            Number of records deleted
        """
        async with self.pool.acquire() as conn:
            try:
                deleted_count = await conn.fetchval(
                    "SELECT cleanup_old_metrics($1)", retention_days
                )
            except asyncpg.exceptions.UndefinedFunctionError:
                # Fallback to manual deletion
                cutoff_date = datetime.now(timezone.utc) - timedelta(
                    days=retention_days
                )
                result = await conn.execute(
                    "DELETE FROM metrics_timeseries WHERE timestamp < $1", cutoff_date
                )
                # Parse "DELETE N" to get count
                deleted_count = int(result.split()[-1]) if result else 0

        logger.info("old_metrics_cleaned", deleted_count=deleted_count)

        return cast(int, deleted_count)

    async def get_metrics_by_dimensions(
        self,
        tenant_id: str,
        project_id: str,
        metric_name: str,
        dimensions: Dict[str, Any],
        start_time: datetime,
        end_time: datetime,
    ) -> List[Dict[str, Any]]:
        """
        Get metrics filtered by specific dimension values.

        Args:
            tenant_id: Tenant identifier
            project_id: Project identifier
            metric_name: Metric name
            dimensions: Dictionary of dimension filters
            start_time: Start of time range
            end_time: End of time range

        Returns:
            List of matching metric records
        """
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT timestamp, value, dimensions, tags
                FROM metrics_timeseries
                WHERE tenant_id = $1
                  AND project_id = $2
                  AND metric_name = $3
                  AND timestamp BETWEEN $4 AND $5
                  AND dimensions @> $6::jsonb
                ORDER BY timestamp DESC
                """,
                tenant_id,
                project_id,
                metric_name,
                start_time,
                end_time,
                json.dumps(dimensions),
            )

        return [dict(r) for r in records]
