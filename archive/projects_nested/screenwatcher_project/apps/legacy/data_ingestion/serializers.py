"""
Serializers for the data ingestion app.
"""
from __future__ import annotations

from rest_framework import serializers

from .models import DataLog


class DataLogSerializer(serializers.ModelSerializer):
    roi_name = serializers.ReadOnlyField(source='roi.name')

    class Meta:
        model = DataLog
        fields = ['id', 'roi', 'roi_name', 'timestamp', 'value']