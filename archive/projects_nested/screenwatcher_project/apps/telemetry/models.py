from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.fields import LegacyJSONField


class TelemetryPoint(models.Model):
    machine = models.ForeignKey('registry.Machine', on_delete=models.CASCADE, related_name='telemetry_points')
    timestamp = models.DateTimeField(db_index=True)
    kind = models.CharField(max_length=32, db_index=True, default='raw')
    payload = models.JSONField()  # Stores raw data: {"speed": 100, "temp": 55, "metrics": {"ink": 10}}
    
    class Meta:
        indexes = [
            models.Index(fields=['machine', 'timestamp', 'kind']),
        ]
        ordering = ['-timestamp']

class MetricDefinition(models.Model):
    """
    Defines a type of data that can be visualized.
    Examples:
    - Name: 'Zużycie Energii', Key: 'energy_kwh', Unit: 'kWh'
    - Name: 'Prędkość', Key: 'speed', Unit: 'm/min'
    """
    name = models.CharField(max_length=100, help_text="Display name (e.g., 'Ink Consumption')")
    code = models.SlugField(max_length=50, unique=True, help_text="Internal ID (e.g., 'ink_usage')")
    json_key = models.CharField(max_length=200, help_text="Path in JSON payload (e.g., 'metrics.ink' or 'speed')")
    unit = models.CharField(max_length=20, blank=True, help_text="Unit symbol (e.g., 'kg', 'm2', '°C')")
    
    AGGREGATION_CHOICES = [('avg', 'Average'), ('sum', 'Sum'), ('max', 'Max'), ('min', 'Min')]
    aggregation = models.CharField(max_length=10, choices=AGGREGATION_CHOICES, default='avg')

    def __str__(self):
        return f"{self.name} [{self.unit}]"


class TelemetryHourlyRollup(models.Model):
    """
    Aggregated telemetry data per hour for performance and historical analysis.
    """
    machine = models.ForeignKey(
        'registry.Machine',
        on_delete=models.CASCADE,
        related_name='hourly_rollups'
    )
    timestamp = models.DateTimeField(db_index=True, help_text=_("Start of the hour"))
    kind = models.CharField(max_length=32, db_index=True)
    
    # Statistics
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    avg_value = models.FloatField(null=True, blank=True)
    sum_value = models.FloatField(null=True, blank=True)
    count_points = models.IntegerField(default=0)
    
    # New flexible storage for multiple metrics
    metrics_summary = models.JSONField(default=dict, blank=True, help_text="Aggregated metrics e.g. {'ink_drops': 500, 'area_m2': 12}")

    class Meta:
        unique_together = ('machine', 'timestamp', 'kind')
        indexes = [
            models.Index(fields=['machine', 'timestamp', 'kind']),
        ]

    def __str__(self):
        return f"Rollup {self.machine.code} - {self.kind} @ {self.timestamp}"
