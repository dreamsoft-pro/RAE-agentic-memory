from django.views.generic import TemplateView
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from datetime import timedelta, datetime
import json
import logging
from django.db import models
from .models import Dashboard, Widget
from apps.registry.models import Machine
from apps.rbac.services import EnforcerService
from apps.rbac.permissions import CasbinPermission
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import DashboardSerializer, WidgetSerializer, MachineStatsSerializer
from apps.oee.services import OEEMetricsService
from apps.telemetry.models import TelemetryPoint
from apps.oee.models import DailyOEE

logger = logging.getLogger("django")

class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated, CasbinPermission]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Dashboard.objects.all()
        return Dashboard.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=["post"])
    def save_layout(self, request, pk=None):
        dashboard = self.get_object()
        widgets_data = request.data.get("widgets", [])
        incoming_ids = [w["id"] for w in widgets_data if w.get("id") and not str(w["id"]).startswith("new")]
        Widget.objects.filter(dashboard=dashboard).exclude(id__in=incoming_ids).delete()
        for w_data in widgets_data:
            w_id = w_data.get("id")
            if not w_id or str(w_id).startswith("new"):
                Widget.objects.create(dashboard=dashboard, widget_type=w_data["type"], title=w_data["title"], pos_x=w_data["x"], pos_y=w_data["y"], width=w_data["w"], height=w_data["h"], config=w_data.get("config", {}))
            else:
                Widget.objects.filter(id=w_id, dashboard=dashboard).update(pos_x=w_data["x"], pos_y=w_data["y"], width=w_data["w"], height=w_data["h"], config=w_data.get("config", {}))
        return Response({"status": "layout saved"})

class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated, CasbinPermission]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Widget.objects.all()
        return Widget.objects.filter(dashboard__user=self.request.user)

class DashboardView(TemplateView):
    template_name = "dashboards/builder_v5.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["machines"] = Machine.objects.filter(is_active=True)
        dashboard_id = self.kwargs.get("dashboard_id")
        
        if self.request.user.is_authenticated:
            if dashboard_id:
                # Allow access if: Owner OR Superuser OR Public
                try:
                    dashboard = Dashboard.objects.get(id=dashboard_id)
                    # Check permissions
                    if not (dashboard.user == self.request.user or self.request.user.is_superuser or dashboard.is_public):
                         # If found but no permission, treat as 404 to avoid leaking existence? 
                         # Or 403. For now, sticking to 404 behavior or just letting the previous logic handle it if stricter.
                         # But here we want to ALLOW.
                         from django.http import Http404
                         raise Http404("No Dashboard matches the given query.")
                except Dashboard.DoesNotExist:
                     from django.http import Http404
                     raise Http404("No Dashboard matches the given query.")
            else:
                dashboard = Dashboard.objects.filter(user=self.request.user, is_default=True).first()
                if not dashboard:
                    dashboard = Dashboard.objects.create(user=self.request.user, is_default=True, name="My Main Dashboard")
            
            context["dashboard"] = dashboard
            all_widgets = Widget.objects.filter(dashboard=dashboard)
            widgets_data = []
            for w in all_widgets:
                widgets_data.append({"id": str(w.id), "type": w.widget_type, "title": w.title, "x": w.pos_x, "y": w.pos_y, "w": w.width, "h": w.height, "config": w.config})
            context["widgets_json"] = json.dumps(widgets_data, cls=DjangoJSONEncoder)
        else:
            context["widgets_json"] = "[]"
        return context

class MachineStatsAPI(APIView):
    def get(self, request, pk):
        machine = get_object_or_404(Machine, pk=pk)
        metrics_service = OEEMetricsService()
        oee_data = metrics_service.calculate_machine_oee(machine)
        return Response({"machine": {"id": str(machine.id), "name": machine.name, "status": "RUNNING"}, "oee": oee_data})

class ReliabilityMetricsAPI(APIView):
    def get(self, request, pk):
        return Response({"availability": 95.5, "performance": 88.2, "quality": 99.1})

class TelemetryTrendAPI(APIView):
    def get(self, request, pk):
        # pk is machine_id
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=24)
        
        points = TelemetryPoint.objects.filter(
            machine_id=pk,
            timestamp__range=(start_date, end_date)
        ).values('timestamp', 'payload')
        
        hourly_data = {}
        
        for p in points:
            ts = p['timestamp']
            # Round to hour
            hour_key = ts.replace(minute=0, second=0, microsecond=0)
            
            payload = p['payload']
            prod = payload.get('metrics', {}).get('parts_delta', 0)
            if not prod:
                 prod = payload.get('production_count', 0)
            
            try:
                val = float(prod)
                # Sum per hour
                if hour_key in hourly_data:
                    hourly_data[hour_key] += val
                else:
                    hourly_data[hour_key] = val
            except (ValueError, TypeError):
                pass
                
        # Format for frontend: {"data": [{"t": iso, "v": val}]}
        sorted_keys = sorted(hourly_data.keys())
        data = [{"t": k.isoformat(), "v": hourly_data[k]} for k in sorted_keys]
        
        return Response({"data": data})

class AggregateMetricsAPI(APIView):
    def get(self, request):
        return Response({"total_production": 5000, "avg_oee": 82.5})

class TelemetrySeriesAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        machine_id = request.query_params.get('machine_id')
        metric = request.query_params.get('metric') # e.g., 'speed', 'temperature'
        start_str = request.query_params.get('from')
        end_str = request.query_params.get('to')

        print(f"DEBUG: TelemetrySeriesAPI machine={machine_id} metric={metric}")

        if not machine_id:
            return Response({"error": "machine_id required"}, status=400)

        # Parse dates
        try:
            if start_str:
                start_date = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            else:
                start_date = timezone.now() - timedelta(hours=24)
            
            if end_str:
                end_date = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            else:
                end_date = timezone.now()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=400)

        # Optimize Query
        points_qs = TelemetryPoint.objects.filter(
            machine_id=machine_id,
            timestamp__range=(start_date, end_date)
        ).values('timestamp', 'payload').order_by('timestamp')

        total_points = points_qs.count()
        print(f"DEBUG: Found {total_points} points for {machine_id}")
        
        # Limit to last 2000 if too many
        if total_points > 2000:
            # Slicing a QuerySet with .values() returns a new QuerySet (limit/offset)
            # But negative indexing is not supported on QuerySet constraints?
            # Actually [start:stop] is supported.
            # To get LAST N, we can order by -timestamp, take N, then reverse?
            # Or count-N : count.
            # Let's try simple python slicing if count is known, but that might load IDs.
            # Safer: Order by -timestamp, limit 2000, then reverse list in python.
            points_qs = TelemetryPoint.objects.filter(
                machine_id=machine_id,
                timestamp__range=(start_date, end_date)
            ).values('timestamp', 'payload').order_by('-timestamp')[:2000]
            # Will need to reverse later for chart
        
        # Convert to list to iterate (and reverse if needed)
        points_list = list(points_qs)
        if total_points > 2000:
            points_list.reverse() # Restore chronological order

        data = []
        for p in points_list:
            val = None
            payload = p['payload']
            if metric:
                val = payload.get('metrics', {}).get(metric)
                if val is None:
                    val = payload.get(metric)
            else:
                val = payload.get('metrics', {}).get('speed')

            if val is not None:
                try:
                    val = float(val)
                    # Hack: hard limit for OCR noise on speed
                    if metric == 'clean_speed' and val > 450.0:
                        continue
                    
                    data.append({
                        "t": p['timestamp'].isoformat(),
                        "v": val
                    })
                except (ValueError, TypeError):
                    pass
        
        print(f"DEBUG: Returning {len(data)} data points")
        return Response({"data": data})

class StatusHistoryAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        machine_id = request.query_params.get('machine_id')
        start_str = request.query_params.get('from')
        end_str = request.query_params.get('to')
        
        if not machine_id:
            return Response({"error": "machine_id required"}, status=400)

        try:
            if start_str:
                start_date = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            else:
                start_date = timezone.now() - timedelta(hours=24)
            
            if end_str:
                end_date = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            else:
                end_date = timezone.now()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=400)

        # Logic from MachineGanttProvider (Telemetry based)
        points = TelemetryPoint.objects.filter(
            machine_id=machine_id, 
            timestamp__range=(start_date, end_date)
        ).order_by('timestamp')
        
        # Optimization for large datasets
        if points.count() > 5000:
            points = points.iterator()

        import re
        def get_strict_status(p):
            payload = p.payload
            val = payload.get('Speed')
            
            # Fallback to OCR table / poles
            if not val:
                metrics = payload.get('metrics', {})
                val = metrics.get('pole_5') # Speed is usually pole_5 in ScreenWatcher JSONL
            
            speed = 0.0
            # Try parsed clean_speed first
            if payload.get('clean_speed', 0) > 0:
                speed = payload.get('clean_speed')
            elif val:
                try:
                    if isinstance(val, (int, float)): speed = float(val)
                    elif isinstance(val, str):
                        # Extract number from format like "239.63 m2 / (45.2 m)/h"
                        m = re.search(r'([\d\.]+)', val.replace(',', '.'))
                        if m: speed = float(m.group(1))
                except: pass
            
            if speed > 10.0: return 'JOB: Running'
            if speed > 0.0: return 'MICRO-STOP'
            return 'STOPPED'

        history = []
        cur = None
        
        # Color Map (Backend fallback, though frontend overrides it)
        colors = {
            'JOB: Running': '#91cc75',
            'STOPPED': '#ef4444',
            'MICRO-STOP': '#f59e0b',
            'NO-DATA': '#e5e7eb'
        }

        try:
            for p in points:
                status = get_strict_status(p)
                ts = p.timestamp
                
                if cur is None:
                    cur = {'name': status, 'start': ts, 'end': ts}
                else:
                    gap = (ts - cur['end']).total_seconds()
                    
                    if status == cur['name'] and gap < 300:
                        cur['end'] = ts
                    else:
                        # Close current segment
                        history.append({
                            "name": cur['name'],
                            "value": [0, cur['start'].isoformat(), cur['end'].isoformat(), (cur['end'] - cur['start']).total_seconds() * 1000],
                            "itemStyle": {"color": colors.get(cur['name'], '#999')}
                        })
                        
                        # Add gap if significant
                        if gap > 300:
                            history.append({
                                "name": "NO-DATA",
                                "value": [0, cur['end'].isoformat(), ts.isoformat(), gap * 1000],
                                "itemStyle": {"color": colors['NO-DATA']}
                            })
                        
                        cur = {'name': status, 'start': ts, 'end': ts}
            
            # Close final segment
            if cur:
                history.append({
                    "name": cur['name'],
                    "value": [0, cur['start'].isoformat(), cur['end'].isoformat(), (cur['end'] - cur['start']).total_seconds() * 1000],
                    "itemStyle": {"color": colors.get(cur['name'], '#999')}
                })
                
        except Exception as e:
            print(f"Gantt Build Error: {e}")

        return Response({"data": history})

from apps.dashboards.services.widget_data import WidgetDataService

class WidgetDataAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        import sys
        try:
            widget = Widget.objects.get(pk=pk)
            sys.stderr.write(f"API DEBUG: Requesting data for Widget {pk} (Type: {widget.widget_type})\n")
        except Widget.DoesNotExist:
            return Response({"error": "Widget not found"}, status=404)
            
        data = WidgetDataService.get_widget_data(widget, request.query_params)
        return Response(data)
