"""
WSGI config for the ScreenWatcher project.

This module exposes the WSGI callable required by Django's deployment
mechanism. It exists so that web servers can point to this file to
initialize the application.
"""
import os
from django.core.wsgi import get_wsgi_application  # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')

application = get_wsgi_application()