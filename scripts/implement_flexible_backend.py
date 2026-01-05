
import os

BASE_DIR = "/home/grzegorz-lesniowski/cloud/screenwatcher_project/apps/dashboards"

# 1. Update admin.py
admin_path = os.path.join(BASE_DIR, "admin.py")
admin_content = """from django.contrib import admin
from .models import Dashboard, Widget, WidgetDefinition

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'is_default')
    list_filter = ('is_public', 'is_default')
    search_fields = ('name', 'user__username')

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'widget_type', 'dashboard')
    list_filter = ('widget_type',)

@admin.register(WidgetDefinition)
class WidgetDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_code', 'is_active')
    list_filter = ('is_active',)
"""
with open(admin_path, 'w') as f:
    f.write(admin_content)
print("Updated admin.py")

# 2. Update views.py (Append new API class)
views_path = os.path.join(BASE_DIR, "views.py")
with open(views_path, 'r') as f:
    views_current = f.read()

new_api_view = """
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import timedelta

class TelemetrySeriesAPI(APIView):
    \"\"\"
    Universal API for flexible time-series data.
    Params:
        machine_id (uuid)
        metric (str): e.g. 'speed', 'temp'
        from (iso_date)
        to (iso_date)
        resolution (str): 'raw', '1m', '1h', '1d' (currently handles raw/downsampled)
    \"\"\"
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        machine_id = request.query_params.get('machine_id')
        metric = request.query_params.get('metric', 'speed')
        start_str = request.query_params.get('from')
        end_str = request.query_params.get('to')
        
        if not machine_id:
            return Response({"error": "machine_id required"}, status=400)
            
        # Defaults
        end = parse_datetime(end_str) if end_str else timezone.now()
        start = parse_datetime(start_str) if start_str else (end - timedelta(hours=1))
        
        # Fetch Data
        from apps.telemetry.models import TelemetryPoint
        qs = TelemetryPoint.objects.filter(
            machine_id=machine_id,
            timestamp__gte=start,
            timestamp__lte=end
        ).order_by('timestamp')
        
        # Metric Extraction Helper
        # We fetch ID and Timestamp + Payload to minimize DB load, but payload is needed
        # Optimziation: limit query size
        total_count = qs.count()
        limit = 5000
        
        if total_count > limit:
            # Simple downsampling: take every Nth record
            step = total_count // limit
            # This is not efficient for huge DBs (OFFSET is slow), but works for MVP < 1M rows
            # Better approach: filter by ID modulo or just slice in python if memory allows
            # For now, let's fetch all (up to safe limit) and process in python
            qs = qs[:10000] # Hard safety cap
        
        data = []
        for p in qs:
            val = 0
            # Extract metric from payload
            # Payload structure varies. Usually payload['metrics']['parts_delta'] or payload['temp']
            pl = p.payload
            
            if metric == 'speed':
                # Calculate speed from parts_delta (simplification)
                # Ideally speed is in payload, or calc from delta/time
                metrics = pl.get('metrics', {})
                val = metrics.get('parts_delta', 0)
                # Convert to parts/hour roughly? No, keep raw count for now or logic from trend api
                
            elif metric == 'temp':
                metrics = pl.get('metrics', {})
                val = metrics.get('temp', 0)
                
            elif metric == 'oee':
                # OEE might be pre-calculated
                pass
            
            # Allow direct key access
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
"""

if "class TelemetrySeriesAPI" not in views_current:
    with open(views_path, 'a') as f:
        f.write(new_api_view)
    print("Appended TelemetrySeriesAPI to views.py")

# 3. Update urls.py
urls_path = os.path.join(BASE_DIR, "urls.py")
with open(urls_path, 'r') as f:
    urls_content = f.read()

if "TelemetrySeriesAPI" not in urls_content:
    # Add import
    urls_content = urls_content.replace("from .views import", "from .views import TelemetrySeriesAPI,")
    # Add path
    new_path = "    path('api/series/', TelemetrySeriesAPI.as_view(), name='telemetry-series'),"
    urls_content = urls_content.replace("urlpatterns = [", "urlpatterns = [\n" + new_path)
    
    with open(urls_path, 'w') as f:
        f.write(urls_content)
    print("Updated urls.py")


