from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class Dashboard(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='dashboards'
    )
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class WidgetDefinition(BaseModel):
    # Defines available widget types in the system, manageable via Admin.
    type_code = models.CharField(max_length=50, unique=True, help_text="Unique code, e.g., 'production_trend'")
    name = models.CharField(max_length=100, help_text="Display name")
    description = models.TextField(blank=True)
    default_config = models.JSONField(default=dict, help_text="Default configuration (JSON)")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Widget(BaseModel):
    WIDGET_TYPES = [
        ('oee_gauge', 'OEE Gauge'),
        ('production_trend', 'Production Trend'),
        ('oee_trend', 'OEE Trend Line'),
        ('oee_bar', 'OEE Components Bar'),
        ('downtime_pareto', 'Downtime Pareto'),
        ('status_card', 'Machine Status Card'),
        ('machine_gantt', 'Machine Status Gantt'),
        ('reliability_card', 'Reliability (MTBF/MTTR)'),
        ('oee_heatmap', 'OEE Heatmap (Lines vs Time)'),
        ('alerts_list', 'Recent Alerts List'),
        ('multi_series_chart', 'Multi-Series Chart (Custom)'),
    ]

    dashboard = models.ForeignKey(
        Dashboard, 
        on_delete=models.CASCADE, 
        related_name='widgets'
    )
    title = models.CharField(max_length=100, blank=True)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    
    # Configuration
    # We store machine_id, time_range, aggregation, etc. in a JSON field for maximum flexibility
    config = models.JSONField(default=dict, help_text="Configuration for the widget (machine_id, range, etc.)")
    
    # Layout (Gridstack.js or similar)
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)
    width = models.IntegerField(default=4)
    height = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.widget_type} on {self.dashboard.name}"

class WidgetSeries(models.Model):
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='series')
    metric = models.ForeignKey('telemetry.MetricDefinition', on_delete=models.CASCADE)
    machine = models.ForeignKey('registry.Machine', on_delete=models.CASCADE)
    
    label = models.CharField(max_length=50, blank=True, help_text="Override metric name (optional)")
    y_axis = models.CharField(max_length=10, choices=[('left', 'Left'), ('right', 'Right')], default='left')
    chart_type = models.CharField(max_length=20, choices=[('line', 'Line'), ('bar', 'Bar'), ('scatter', 'Scatter')], default='line')
    color = models.CharField(max_length=7, blank=True, help_text="Hex color (e.g. #ff0000)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.label or self.metric.name} ({self.machine.code})"
