from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.registry.models import Machine

class DataImport(models.Model):
    class ImportType(models.TextChoices):
        SCREENWATCHER_JSONL = 'sw_jsonl', _('ScreenWatcher JSONL (OCR)')
        MACHINE_LOG_CSV = 'machine_csv', _('Machine Log CSV')

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='data_imports')
    import_file = models.FileField(upload_to='imports/%Y/%m/%d/')
    import_type = models.CharField(max_length=20, choices=ImportType.choices, default=ImportType.SCREENWATCHER_JSONL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    log = models.TextField(blank=True, help_text="Processing logs and errors")

    def __str__(self):
        return f"{self.machine.code} - {self.get_import_type_display()} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class MetricReading(models.Model):
    """
    Universal table for numeric timeseries data (Long Format).
    Optimized for Grafana querying.
    """
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='metrics')
    timestamp = models.DateTimeField(db_index=True)
    
    # Name of the metric (e.g., 'speed_m2h', 'ink_ml', 'power_kW')
    name = models.CharField(max_length=100, db_index=True)
    
    # Numeric value
    value = models.FloatField()
    
    # Optional grouping ID (to link metrics from the same reading/file line)
    group_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            # Compound index for fast Grafana queries: "Give me 'speed' for 'MachineA' in time range X-Y"
            models.Index(fields=['machine', 'name', 'timestamp']),
        ]
        verbose_name = _("Metric Reading")
        verbose_name_plural = _("Metric Readings")

    def __str__(self):
        return f"{self.machine.code} | {self.timestamp} | {self.name}={self.value}"


class MetricContext(models.Model):
    """
    Universal table for text/categorical metadata (Context).
    Stores statuses, filenames, order IDs, etc.
    """
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='contexts')
    timestamp = models.DateTimeField(db_index=True)
    
    # Context key (e.g., 'status', 'job_file', 'order_id')
    key = models.CharField(max_length=100, db_index=True)
    
    # Text value
    value = models.TextField()
    
    group_id = models.UUIDField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['machine', 'key', 'timestamp']),
        ]
        verbose_name = _("Metric Context")
        verbose_name_plural = _("Metric Contexts")

    def __str__(self):
        return f"{self.machine.code} | {self.timestamp} | {self.key}={self.value[:50]}"