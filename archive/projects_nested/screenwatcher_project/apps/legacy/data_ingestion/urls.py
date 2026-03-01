"""
URL routing for the data ingestion app.

Exposes a simple POST endpoint at ``/api/ingest/`` for clients to push
captured data. Also registers a read‑only viewset under ``/api/ingest/logs/``
for retrieving stored data.
"""
from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import DataIngestionView, DataLogViewSet

app_name = 'data-ingestion'

router = DefaultRouter()
router.register(r'logs', DataLogViewSet)

urlpatterns = [
    path('', DataIngestionView.as_view(), name='ingest'),
    path('', include(router.urls)),
]