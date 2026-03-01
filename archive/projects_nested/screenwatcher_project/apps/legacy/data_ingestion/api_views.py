"""
API views for the data ingestion app.

Provides an endpoint to accept data from ScreenWatcher clients and to
list or retrieve ingested data.
"""
from __future__ import annotations

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.configurator.models import RegionOfInterest
from .models import DataLog
from .serializers import DataLogSerializer
from apps.data_forwarding.tasks import push_data


class DataIngestionView(APIView):
    """Accepts POST requests with ROI name and data payload for ingestion."""

    def post(self, request, *args, **kwargs):
        roi_name = request.data.get('roi_name')
        data = request.data.get('data')
        if not roi_name:
            return Response({'detail': 'Parameter "roi_name" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            roi = RegionOfInterest.objects.get(name=roi_name)
        except RegionOfInterest.DoesNotExist:
            return Response({'detail': f'RegionOfInterest "{roi_name}" not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Create a DataLog entry. ``value`` can be arbitrary JSON or string.
        datalog = DataLog.objects.create(roi=roi, value=data)
        # Trigger asynchronous forwarding.
        push_data.delay(datalog.id)
        serializer = DataLogSerializer(datalog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DataLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows listing and retrieving stored data logs via the API."""

    queryset = DataLog.objects.select_related('roi', 'roi__application').all()
    serializer_class = DataLogSerializer