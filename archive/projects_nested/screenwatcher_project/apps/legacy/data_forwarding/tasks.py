"""
Celery tasks for the data forwarding app.

Defines a task to forward ingested data to any configured external systems.
The mapping between regions of interest and external systems is defined in
``RegionExternalSystem``. Depending on the method, the task uses HTTP or
MQTT to deliver the payload. Exceptions are swallowed but logged for
operational visibility.
"""
from __future__ import annotations

import json
from typing import Any, Dict

from celery import shared_task  # type: ignore

from .models import ExternalSystem, RegionExternalSystem
from apps.data_ingestion.models import DataLog

try:
    import httpx  # type: ignore
except ImportError:
    httpx = None  # type: ignore

try:
    import paho.mqtt.publish as mqtt_publish  # type: ignore
except ImportError:
    mqtt_publish = None  # type: ignore


@shared_task(bind=True, ignore_result=True)
def push_data(self, datalog_id: int) -> None:
    """Push a DataLog instance to all external systems mapped to its ROI."""
    try:
        datalog = DataLog.objects.select_related('roi').get(pk=datalog_id)
    except DataLog.DoesNotExist:
        return

    # Build a generic payload
    payload: Dict[str, Any] = {
        'roi_name': datalog.roi.name,
        'application_name': datalog.roi.application.name,
        'timestamp': datalog.timestamp.isoformat(),
        'value': datalog.value,
    }

    # Retrieve all external systems associated with this ROI
    mappings = RegionExternalSystem.objects.select_related('external_system').filter(roi=datalog.roi)
    for mapping in mappings:
        system: ExternalSystem = mapping.external_system
        cfg = system.config or {}
        method = system.method
        try:
            if method in (ExternalSystem.METHOD_API, ExternalSystem.METHOD_WEBHOOK):
                if httpx is None:
                    continue
                url = cfg.get('url')
                http_method = cfg.get('http_method', 'POST').upper()
                headers = cfg.get('headers', {})
                timeout = cfg.get('timeout', 10)
                if not url:
                    continue
                if http_method == 'POST':
                    httpx.post(url, json=payload, headers=headers, timeout=timeout)
                elif http_method == 'PUT':
                    httpx.put(url, json=payload, headers=headers, timeout=timeout)
                else:
                    # Default to POST for unsupported methods
                    httpx.post(url, json=payload, headers=headers, timeout=timeout)
            elif method == ExternalSystem.METHOD_MQTT:
                if mqtt_publish is None:
                    continue
                host = cfg.get('host', 'localhost')
                port = int(cfg.get('port', 1883))
                topic = cfg.get('topic')
                username = cfg.get('username')
                password = cfg.get('password')
                if not topic:
                    continue
                mqtt_kwargs = {'hostname': host, 'port': port}
                if username and password:
                    mqtt_kwargs.update({'auth': {'username': username, 'password': password}})
                mqtt_publish.single(topic, payload=json.dumps(payload), **mqtt_kwargs)
        except Exception as exc:
            # Log the exception somewhere (omitted for brevity)
            print(f"Error forwarding data to {system.name}: {exc}")  # pragma: no cover