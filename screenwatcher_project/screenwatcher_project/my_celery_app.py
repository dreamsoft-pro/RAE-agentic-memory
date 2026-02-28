"""
Celery configuration for ScreenWatcher.

This module defines a Celery application and configures it to load
Django settings, schedule periodic tasks, and use Django's settings
for broker and result backend. Importing this module in
``screenwatcher_project/__init__.py`` ensures the application is loaded
when Django starts.
"""
from __future__ import annotations

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')

app = Celery('screenwatcher_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self, *args, **kwargs):
    """A simple debug task that prints request details when executed."""
    print(f'Request: {self.request!r}')  # pragma: no cover