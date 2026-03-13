from django.db import models
from apps.core.models import BaseModel
from apps.registry.models import Machine, Shift
from apps.operator_panel.models import ReasonCode

class DailyOEE(BaseModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='daily_oee')
    date = models.DateField(db_index=True)
    
    # Components (0.0 - 100.0)
    availability = models.FloatField(default=0.0)
    performance = models.FloatField(default=0.0)
    quality = models.FloatField(default=0.0)
    
    # Result
    oee = models.FloatField(default=0.0)
    
    # Raw Data for drill-down (optional)
    total_time_min = models.IntegerField(default=1440) # 24h
    run_time_min = models.IntegerField(default=0)
    total_parts = models.IntegerField(default=0)
    good_parts = models.IntegerField(default=0)

    class Meta:
        unique_together = ('machine', 'date')
        ordering = ['-date']

    def calculate_oee(self):
        """Re-calculates OEE based on components."""
        self.oee = (self.availability * self.performance * self.quality) / 10000.0
        return self.oee

    def __str__(self):
        return f"OEE {self.machine.code} {self.date}: {self.oee:.1f}%"

class ShiftOEE(BaseModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='shift_oee')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField(db_index=True) # The date the shift *started*
    
    # Components
    availability = models.FloatField(default=0.0)
    performance = models.FloatField(default=0.0)
    quality = models.FloatField(default=0.0)
    
    # Result
    oee = models.FloatField(default=0.0)
    
    # Raw Data
    total_time_min = models.IntegerField(default=480) # 8h typical
    run_time_min = models.IntegerField(default=0)
    total_parts = models.IntegerField(default=0)
    good_parts = models.IntegerField(default=0)

    class Meta:
        unique_together = ('machine', 'shift', 'date')
        ordering = ['-date', 'shift__start_time']

    def calculate_oee(self):
        self.oee = (self.availability * self.performance * self.quality) / 10000.0
        return self.oee

    def __str__(self):
        return f"OEE {self.machine.code} {self.date} {self.shift.name}: {self.oee:.1f}%"

class DowntimeEvent(BaseModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='downtime_events')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    
    reason = models.ForeignKey(ReasonCode, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_time']
        
    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            self.duration_seconds = int(delta.total_seconds())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.machine.code} STOP {self.start_time} ({self.duration_seconds}s)"

class ProductionJob(BaseModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='production_jobs')
    timestamp = models.DateTimeField(db_index=True)
    task_name = models.CharField(max_length=255)
    
    print_area = models.FloatField(default=0.0, help_text="m2")
    print_length = models.FloatField(default=0.0, help_text="m")
    
    time_consuming_h = models.FloatField(default=0.0)
    ink_consumption_ml = models.FloatField(default=0.0)
    
    is_cancelled = models.BooleanField(default=False)
    
    # Optional fields for metrics
    finish_total_ratio = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('machine', 'timestamp', 'task_name')

    def __str__(self):
        return f"Job {self.task_name} on {self.machine.code} @ {self.timestamp}"