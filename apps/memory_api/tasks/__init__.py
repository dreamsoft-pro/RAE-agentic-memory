"""Celery tasks for RAE Memory API."""

from apps.memory_api.celery_app import celery_app as celery

__all__ = ["celery"]
