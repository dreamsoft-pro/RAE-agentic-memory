import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from django.utils import timezone
from apps.oee.models import DailyOEE
from apps.rules.models import RuleHit
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API to retrieve generated reports.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'report_type': ['exact'],
        'date': ['exact', 'gte', 'lte'],
    }

class ExportOEEView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={(200, 'text/csv'): OpenApiTypes.BINARY})
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="oee_report_{timezone.now().date()}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Machine', 'Availability', 'Performance', 'Quality', 'OEE', 'Total Parts', 'Run Time'])

        records = DailyOEE.objects.select_related('machine').all().order_by('-date', 'machine__code')
        for r in records:
            writer.writerow([
                r.date, 
                r.machine.code, 
                f"{r.availability:.2f}", 
                f"{r.performance:.2f}", 
                f"{r.quality:.2f}", 
                f"{r.oee:.2f}",
                r.total_parts,
                r.run_time_min
            ])

        return response

class ExportEventsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={(200, 'text/csv'): OpenApiTypes.BINARY})
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="events_report_{timezone.now().date()}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Timestamp', 'Machine', 'Rule', 'Payload', 'Actions'])

        records = RuleHit.objects.select_related('machine', 'rule').all().order_by('-created_at')
        for r in records:
            writer.writerow([
                r.created_at, 
                r.machine.code, 
                r.rule.name, 
                r.payload,
                r.action_log
            ])

        return response
