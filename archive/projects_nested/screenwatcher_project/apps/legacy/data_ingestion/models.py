"""
Models for the data ingestion app.

Captures data emitted by ScreenWatcher clients and associates it with a
RegionOfInterest. Values are stored as JSON to accommodate either
unstructured text or structured tables.
"""
from __future__ import annotations

from django.db import models


class DataLog(models.Model):
    """A log entry representing a single data point captured from a client."""

    roi = models.ForeignKey('configurator.RegionOfInterest', related_name='data_logs', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Data Log'
        verbose_name_plural = 'Data Logs'

    def __str__(self) -> str:
        return f"{self.roi.name} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"