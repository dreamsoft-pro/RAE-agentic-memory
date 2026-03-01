from django.db import models
from apps.core.models import BaseModel

class Report(BaseModel):
    REPORT_TYPES = [
        ('SHIFT_END', 'Shift End Report'),
        ('DAILY_SUMMARY', 'Daily Summary'),
        ('ON_DEMAND', 'On Demand'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    # Context
    date = models.DateField(help_text="The date this report covers")
    shift_name = models.CharField(max_length=50, blank=True, null=True)
    
    # Content
    data = models.JSONField(default=dict, help_text="Structured data of the report")
    file = models.FileField(upload_to='reports/', null=True, blank=True, help_text="Optional PDF/CSV file")

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.report_type} - {self.date} ({self.created_at})"
