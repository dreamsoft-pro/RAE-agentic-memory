"""
Models for the configurator app.

Defines entities for configuring which applications are monitored and the
regions of interest (ROIs) within their user interfaces. An ROI consists
of a rectangular area on a screenshot accompanied by a semantic name and
data type. Screenshots are stored in the ``MEDIA_ROOT``.
"""
from __future__ import annotations

from django.db import models


class TrackedApplication(models.Model):
    """A representation of an application whose screen will be monitored."""

    name = models.CharField(max_length=255, unique=True)
    screenshot = models.ImageField(upload_to='screenshots/')

    class Meta:
        verbose_name = 'Tracked Application'
        verbose_name_plural = 'Tracked Applications'

    def __str__(self) -> str:
        return self.name


class RegionOfInterest(models.Model):
    """Defines a rectangular region on a tracked application's screen."""

    TYPE_LINE = 'line'
    TYPE_TABLE = 'table'
    TYPE_CHOICES = [
        (TYPE_LINE, 'Line'),
        (TYPE_TABLE, 'Table'),
    ]

    name = models.CharField(max_length=255)
    application = models.ForeignKey(TrackedApplication, related_name='rois', on_delete=models.CASCADE)
    x1 = models.PositiveIntegerField(help_text='Left coordinate of ROI (pixels)')
    y1 = models.PositiveIntegerField(help_text='Top coordinate of ROI (pixels)')
    x2 = models.PositiveIntegerField(help_text='Right coordinate of ROI (pixels)')
    y2 = models.PositiveIntegerField(help_text='Bottom coordinate of ROI (pixels)')
    data_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_LINE)

    class Meta:
        unique_together = ('name', 'application')
        verbose_name = 'Region of Interest'
        verbose_name_plural = 'Regions of Interest'

    def __str__(self) -> str:
        return f"{self.name} ({self.application.name})"


class Department(models.Model):
    """Represents a department in a factory."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Line(models.Model):
    """Represents a production line within a department."""
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='lines', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'department')

    def __str__(self) -> str:
        return f"{self.name} ({self.department.name})"


class Machine(models.Model):
    """Represents a machine on a production line."""
    name = models.CharField(max_length=255)
    line = models.ForeignKey(Line, related_name='machines', on_delete=models.CASCADE)
    application = models.OneToOneField(TrackedApplication, related_name='machine', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'line')

    def __str__(self) -> str:
        return f"{self.name} ({self.line.name})"