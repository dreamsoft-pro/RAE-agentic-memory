"""
Models for the data forwarding app.

Defines configuration for external systems (e.g. MES/ERP, webhooks, MQTT
brokers) and maps regions of interest to these systems so that incoming
data can be forwarded appropriately.
"""
from __future__ import annotations

from django.db import models


class ExternalSystem(models.Model):
    """Describes an external system to which data can be forwarded."""

    METHOD_API = 'api'
    METHOD_WEBHOOK = 'webhook'
    METHOD_MQTT = 'mqtt'
    METHOD_CHOICES = [
        (METHOD_API, 'API'),
        (METHOD_WEBHOOK, 'Webhook'),
        (METHOD_MQTT, 'MQTT'),
    ]

    name = models.CharField(max_length=255, unique=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    config = models.JSONField(help_text='Configuration for connecting to the external system.')

    class Meta:
        verbose_name = 'External System'
        verbose_name_plural = 'External Systems'

    def __str__(self) -> str:
        return self.name


class RegionExternalSystem(models.Model):
    """Mapping of RegionOfInterest to ExternalSystem for targeted forwarding."""

    roi = models.ForeignKey('registry.RegionOfInterest', related_name='external_mappings', on_delete=models.CASCADE)
    external_system = models.ForeignKey(ExternalSystem, related_name='roi_mappings', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('roi', 'external_system')
        verbose_name = 'Region External System Mapping'
        verbose_name_plural = 'Region External System Mappings'

    def __str__(self) -> str:
        return f"{self.roi.name} → {self.external_system.name}"