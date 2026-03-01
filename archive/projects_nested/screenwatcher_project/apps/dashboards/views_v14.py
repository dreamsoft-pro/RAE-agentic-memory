from django.views.generic import TemplateView
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.registry.models import Machine
from apps.oee.models import DailyOEE
from apps.telemetry.models import TelemetryPoint
from .models import Dashboard, Widget
from .serializers import MachineStatsSerializer, DashboardSerializer, WidgetSerializer

from rest_framework.decorators import action

from apps.rbac.filters import CasbinFilterBackend
from apps.rbac.services import EnforcerService
from apps.rbac.permissions import CasbinPermission

class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated, CasbinPermission]
    filter_backends = [CasbinFilterBackend]

    def get_queryset(self):
        # Base queryset with optimization
        return Dashboard.objects.prefetch_related('widgets').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def save_layout(self, request, pk=None):
        dashboard = self.get_object()
        layout_data = request.data.get('widgets', [])
        
        # Clear old widgets or update them? Clear and recreate is simpler for a prototype layout
        dashboard.widgets.all().delete()
        
        for w in layout_data:
            Widget.objects.create(
                dashboard=dashboard,
                title=w.get('title', ''),
                widget_type=w.get('type', 'oee_gauge'),
                config=w.get('config', {}),
                pos_x=w.get('x', 0),
                pos_y=w.get('y', 0),
                width=w.get('w', 4),
                height=w.get('h', 4)
            )
            
        return Response({"status": "saved"})

class WidgetViewSet(viewsets.ModelViewSet):
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Widget.objects.filter(dashboard__user=self.request.user)

from django.core.cache import cache

class AggregateMetricsAPI(APIView):
    """
    Powerful API for fetching aggregated OEE metrics for comparison.
    """
    permission_classes = [permissions.IsAuthenticated, CasbinPermission]
    permission_object = 'registry.machine'

    @extend_schema(
        parameters=[
            OpenApiParameter("machine_ids", type=str, description="Comma separated machine IDs"),
            OpenApiParameter("start_date", type=str, description="YYYY-MM-DD"),
            OpenApiParameter("end_date", type=str, description="YYYY-MM-DD"),
            OpenApiParameter("group_by", type=str, description="day, week, month"),
        ]
    )
    def get(self, request):
        # Generate cache key based on params
        cache_key = f"metrics_{request.GET.urlencode()}_{request.user.id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        machine_ids_raw = request.query_params.get('machine_ids', '').split(',')
        machine_ids = [m for m in machine_ids_raw if m]
        
        if not machine_ids:
             return Response([])

        # Filter machine_ids based on Casbin permissions
        sub = request.user.username
        allowed_objs = EnforcerService.get_allowed_objects(sub, 'read')
        
        # Check for global permission or specific machine IDs
        if 'registry.machine' not in allowed_objs:
            # We assume IDs in Casbin are 'machine_ID'
            allowed_machine_ids = [obj.split('_')[1] for obj in allowed_objs if obj.startswith('machine_')]
            machine_ids = [m for m in machine_ids if m in allowed_machine_ids]

        if not machine_ids:
            return Response([], status=status.HTTP_403_FORBIDDEN)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        group_by = request.query_params.get('group_by', 'day')

        queryset = DailyOEE.objects.filter(machine_id__in=machine_ids)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Aggregation logic
        trunc_func = TruncDay
        if group_by == 'week':
            trunc_func = TruncWeek
        elif group_by == 'month':
            trunc_func = TruncMonth

        stats = list(queryset.annotate(period=trunc_func('date')).values('period', 'machine_id').annotate(
            avg_oee=Avg('oee'),
            avg_availability=Avg('availability'),
            avg_performance=Avg('performance'),
            avg_quality=Avg('quality'),
            total_produced=Sum('total_parts')
        ).order_by('period', 'machine_id'))

        # Cache for 5 minutes (300s)
        cache.set(cache_key, stats, 300)

        return Response(stats)

class ReliabilityMetricsAPI(APIView):
    """
    API for reliability metrics (MTBF, MTTR).
    """
    permission_classes = [permissions.IsAuthenticated, CasbinPermission]

    def get(self, request, pk):
        from apps.oee.services import OEEMetricsService
        machine = get_object_or_404(Machine, pk=pk)
        self.check_object_permissions(request, machine)
        
        # Default last 30 days
        end_date = timezone.now()
        start_date = end_date - datetime.timedelta(days=30)
        
        mtbf = OEEMetricsService.calculate_mtbf(machine, start_date, end_date)
        mttr = OEEMetricsService.calculate_mttr(machine, start_date, end_date)
        scrap = OEEMetricsService.calculate_scrap_rate(machine, start_date, end_date)
        
        return Response({
            "mtbf_hours": round(mtbf, 2),
            "mttr_minutes": round(mttr, 2),
            "scrap_rate_percent": round(scrap, 2)
        })

class DashboardView(TemplateView):
    template_name = "dashboards/builder.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch machines filtered by Casbin
        queryset = Machine.objects.filter(is_active=True)
        
        if not self.request.user.is_superuser:
            sub = self.request.user.username
            allowed_objs = EnforcerService.get_allowed_objects(sub, 'read')
            
            if 'registry.machine' not in allowed_objs:
                allowed_ids = [obj.split('_')[1] for obj in allowed_objs if obj.startswith('machine_')]
                queryset = queryset.filter(pk__in=allowed_ids)
        
        context['machines'] = queryset
        
        # Fetch or create default dashboard for the user
        if self.request.user.is_authenticated:
            dashboard, created = Dashboard.objects.get_or_create(
                user=self.request.user,
                is_default=True,
                defaults={'name': 'My Main Dashboard'}
            )
            context['dashboard'] = dashboard
            
            # Serialize widgets to JSON
            widgets_data = []
            for w in dashboard.widgets.all():
                widgets_data.append({
                    'id': str(w.id),
                    'widget_type': w.widget_type,
                    'title': w.title,
                    'pos_x': w.pos_x,
                    'pos_y': w.pos_y,
                    'width': w.width,
                    'height': w.height,
                    'config': w.config
                })
            context['widgets_json'] = json.dumps(widgets_data, cls=DjangoJSONEncoder)
            context['widgets'] = dashboard.widgets.all()
        
        return context

class MachineStatsAPI(APIView):
    """
    API endpoint for ECharts to fetch real-time data.
    """
    permission_classes = [permissions.IsAuthenticated, CasbinPermission]
    
    @extend_schema(responses={200: MachineStatsSerializer})
    def get(self, request, pk):
        machine = get_object_or_404(Machine, pk=pk)
        self.check_object_permissions(request, machine)
        
        today = timezone.now().date()
        
        # Get OEE
        oee_record = DailyOEE.objects.filter(machine=machine, date=today).first()
        oee_data = {
            "oee": oee_record.oee if oee_record else 0,
            "availability": oee_record.availability if oee_record else 0,
            "performance": oee_record.performance if oee_record else 0,
            "quality": oee_record.quality if oee_record else 0
        }
        
        # Get Last Telemetry
        last_tp = TelemetryPoint.objects.filter(machine=machine).first()
        current_status = "OFFLINE"
        last_seen = None
        
        if last_tp:
            current_status = last_tp.payload.get("status", "UNKNOWN")
            last_seen = last_tp.timestamp
            
        return Response({
            "machine": {
                "name": machine.name,
                "code": machine.code,
                "status": current_status,
                "last_seen": last_seen
            },
            "oee": oee_data
        })

class TelemetryTrendAPI(APIView):
    """API for high-resolution production trend (last 10k points)."""
    permission_classes = [permissions.IsAuthenticated]

class TelemetryTrendAPI(APIView):
    """API for high-resolution production trend (last 10k points)."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        from apps.telemetry.models import TelemetryPoint
        from apps.registry.models import Machine

class TelemetryTrendAPI(APIView):
    """API for high-resolution production trend (speed in parts/hour)."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        from apps.telemetry.models import TelemetryPoint
        from apps.registry.models import Machine
        machine = get_object_or_404(Machine, pk=pk)
        

class TelemetryTrendAPI(APIView):
    """API for high-resolution production trend (smoothed speed in parts/hour)."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        from apps.telemetry.models import TelemetryPoint
        from apps.registry.models import Machine
        machine = get_object_or_404(Machine, pk=pk)
        
        # Pobieramy punkty
        points = TelemetryPoint.objects.filter(machine=machine).order_by('-timestamp')[:4000]
        points_list = list(reversed(list(points)))
        
        data = []
        # Okno uśredniania: 6 próbek (przy próbkowaniu co 10s daje to średnią z 1 minuty)
        # To pozwoli uzyskać płynne przejścia między 0 a 360, zamiast skoków.
        # Przy przestoju, po 1 minucie prędkość spadnie do 0.
        window_size = 6 
        speed_buffer = []

        for i in range(1, len(points_list)):
            p_curr = points_list[i]
            p_prev = points_list[i-1]
            
            time_delta = (p_curr.timestamp - p_prev.timestamp).total_seconds()
            if time_delta <= 0.1: continue

            metrics = p_curr.payload.get('metrics', {})
            parts = int(metrics.get('parts_delta', 0)) if 'parts_delta' in metrics else int(p_curr.payload.get('parts_delta', 0))
            
            # Chwilowa prędkość z tego interwału
            inst_speed = (parts / time_delta) * 3600
            
            # Filtrowanie nierealistycznych skoków (np. restart systemu)
            if inst_speed > 20000: inst_speed = 0

            speed_buffer.append(inst_speed)
            if len(speed_buffer) > window_size:
                speed_buffer.pop(0)
            
            avg_speed = sum(speed_buffer) / len(speed_buffer)
            
            # Optimization: save space by skipping points if value didn't change significantly?
            # No, ECharts needs time consistency usually.
            
            data.append({
                "t": p_curr.timestamp,
                "v": round(avg_speed, 1)
            })
             
        return Response(data)

from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import timedelta

class TelemetrySeriesAPI(APIView):
    # Universal API for flexible time-series data.
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        machine_id = request.query_params.get('machine_id')
        metric = request.query_params.get('metric', 'speed')
        start_str = request.query_params.get('from')
        end_str = request.query_params.get('to')
        
        if not machine_id:
            return Response({"error": "machine_id required"}, status=400)
            
        end = parse_datetime(end_str) if end_str else timezone.now()
        start = parse_datetime(start_str) if start_str else (end - timedelta(hours=1))
        
        from apps.telemetry.models import TelemetryPoint
        qs = TelemetryPoint.objects.filter(
            machine_id=machine_id,
            timestamp__gte=start,
            timestamp__lte=end
        ).order_by('timestamp')
        
        total_count = qs.count()
        limit = 5000
        
        if total_count > limit:
            qs = qs[:10000] 
        
        data = []
        for p in qs:
            val = 0
            pl = p.payload
            
            if metric == 'speed':
                metrics = pl.get('metrics', {})
                # Prefer explicit speed metric, fallback to parts_delta * 60 (dummy calc)
                if 'speed' in metrics:
                    val = metrics['speed']
                else:
                    val = metrics.get('parts_delta', 0)
                
            elif metric == 'temp':
                metrics = pl.get('metrics', {})
                val = metrics.get('temp', 0)
            
            elif metric == 'pressure':
                metrics = pl.get('metrics', {})
                val = metrics.get('pressure', 0)

            if val == 0 and metric in pl:
                val = pl[metric]
            
            data.append({
                "t": p.timestamp,
                "v": val
            })
            
        return Response({
            "meta": {
                "count": len(data),
                "metric": metric,
                "start": start,
                "end": end
            },
            "data": data
        })
