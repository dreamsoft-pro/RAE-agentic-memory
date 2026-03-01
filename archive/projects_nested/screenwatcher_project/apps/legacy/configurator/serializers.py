"""
Serializers for the configurator app.

Serializers translate model instances to and from JSON for the API.
"""
from __future__ import annotations

from rest_framework import serializers

from .models import TrackedApplication, RegionOfInterest


class TrackedApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedApplication
        fields = ['id', 'name', 'screenshot']


class RegionOfInterestSerializer(serializers.ModelSerializer):
    application_name = serializers.ReadOnlyField(source='application.name')

    class Meta:
        model = RegionOfInterest
        fields = [
            'id',
            'name',
            'application',
            'application_name',
            'x1', 'y1', 'x2', 'y2',
            'data_type',
        ]