"""
API URL routing for the configurator app.

Registers ``TrackedApplicationViewSet`` and ``RegionOfInterestViewSet``
with a DRF router. The resulting endpoints provide CRUD operations for
tracked applications and ROIs under ``/api/configurator/``.
"""
from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import TrackedApplicationViewSet, RegionOfInterestViewSet

app_name = 'configurator-api'

router = DefaultRouter()
router.register(r'applications', TrackedApplicationViewSet)
router.register(r'rois', RegionOfInterestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]