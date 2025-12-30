
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
    # Add import. Be careful with existing imports.
    # Assuming "from .views import" exists.
    if "from .views import" in urls_content:
        # Simple replace might break if it's a multiline import.
        # Let's try to append the import if possible or just add a new line
        urls_content = "from .views import TelemetrySeriesAPI\n" + urls_content
    
    # Add path
    new_path = "    path('api/series/', TelemetrySeriesAPI.as_view(), name='telemetry-series'),\n"
    if "urlpatterns = [" in urls_content:
        urls_content = urls_content.replace("urlpatterns = [", "urlpatterns = [\n" + new_path)
    
    with open(urls_path, 'w') as f:
        f.write(urls_content)
    print("Updated urls.py")
