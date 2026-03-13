import datetime
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.registry.models import Machine
from .models import DowntimeEvent
from .serializers import DowntimeEventSerializer
from apps.rbac.permissions import CasbinPermission
from apps.rbac.filters import CasbinFilterBackend

from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.core.serializers import MachineTimelineResponseSerializer

class MachineTimelineAPI(APIView):
    """
    Returns a timeline of status changes (RUNNING/STOPPED) for Gantt charts.
    """
    permission_classes = [permissions.IsAuthenticated, CasbinPermission]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='date', description='Date in YYYY-MM-DD format', required=False, type=str),
        ],
        responses={200: MachineTimelineResponseSerializer},
        description="Returns status segments for a specific machine on a given date."
    )
    def get(self, request, pk):
        machine = get_object_or_404(Machine, pk=pk)
        self.check_object_permissions(request, machine)
        
        date_str = request.query_params.get('date', timezone.now().date().isoformat())
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        start_of_day = timezone.make_aware(datetime.datetime.combine(date, datetime.time.min))
        end_of_day = timezone.make_aware(datetime.datetime.combine(date, datetime.time.max))

        # Get all downtime events for this day
        downtimes = DowntimeEvent.objects.filter(
            machine=machine,
            start_time__lt=end_of_day,
            end_time__gt=start_of_day
        ).order_by('start_time') | DowntimeEvent.objects.filter(
            machine=machine,
            start_time__lt=end_of_day,
            end_time__isnull=True
        )

        timeline = []
        # Simplified logic: 
        # For a truly accurate Gantt, we'd need to fill gaps with 'RUNNING'
        # based on TelemetryPoint data. For MVP, we'll return the DowntimeEvents
        # and the UI can infer RUNNING state in between.
        
        for dt in downtimes:
            # Clip to day boundaries
            s = max(dt.start_time, start_of_day)
            e = dt.end_time or timezone.now()
            e = min(e, end_of_day)

            timeline.append({
                "status": "STOPPED",
                "start": s.isoformat(),
                "end": e.isoformat(),
                "reason": dt.reason.description if dt.reason else "Uncategorized",
                "duration": int((e - s).total_seconds())
            })

        return Response({
            "machine": machine.code,
            "date": date_str,
            "events": timeline
        })

class DowntimeEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing downtime events.
    Operators can assign reasons and comments to these events.
    """
    queryset = DowntimeEvent.objects.select_related('machine', 'reason').all()
    serializer_class = DowntimeEventSerializer
    permission_classes = [IsAuthenticated, CasbinPermission]
    filter_backends = [CasbinFilterBackend]

    def get_queryset(self):
        # The FilterBackend handles permission-based filtering
        queryset = super().get_queryset()
        
        # Filtering parameters
        machine_id = self.request.query_params.get('machine', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        uncategorized = self.request.query_params.get('uncategorized', None)

        if machine_id:
            queryset = queryset.filter(machine_id=machine_id)
        
        if start_date:
            queryset = queryset.filter(start_time__date__gte=start_date)
            
        if end_date:
            queryset = queryset.filter(start_time__date__lte=end_date)

        if uncategorized and uncategorized.lower() == 'true':
            queryset = queryset.filter(reason__isnull=True)

        return queryset