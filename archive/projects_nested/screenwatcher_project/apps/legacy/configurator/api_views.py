"""
API views for the configurator app using Django Rest Framework.

Expose CRUD endpoints for tracked applications and regions of interest.
"""
from __future__ import annotations

from rest_framework import viewsets

from .models import TrackedApplication, RegionOfInterest
from .serializers import TrackedApplicationSerializer, RegionOfInterestSerializer


class TrackedApplicationViewSet(viewsets.ModelViewSet):
    """API endpoint for managing ``TrackedApplication`` instances."""

    queryset = TrackedApplication.objects.all()
    serializer_class = TrackedApplicationSerializer


class RegionOfInterestViewSet(viewsets.ModelViewSet):
    """API endpoint for managing ``RegionOfInterest`` instances."""

    queryset = RegionOfInterest.objects.select_related('application').all()
    serializer_class = RegionOfInterestSerializer