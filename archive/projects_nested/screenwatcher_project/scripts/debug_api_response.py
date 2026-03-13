
import os
import sys
import django
import json
from datetime import datetime

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Widget
from apps.dashboards.services.widget_data import WidgetDataService

def debug_response():
    print("--- DEBUG API RESPONSE ---")
    
    # Params from browser logs
    params = {
        'from': '2026-01-19T13:00:00.000Z',
        'to': '2026-01-20T03:00:00.000Z'
    }
    
    # 1. Chart Widget
    w_chart = Widget.objects.filter(title__contains="Wydajność Maszyny").last()
    if w_chart:
        print(f"\n[CHART] {w_chart.title}")
        try:
            data = WidgetDataService.get_widget_data(w_chart, params)
            series = data.get('series', [])
            print(f"Series Count: {len(series)}")
            for s in series:
                points = s.get('data', [])
                print(f" - Series '{s.get('name')}': {len(points)} points")
                if len(points) > 0:
                    print(f"   Sample Point [0]: {points[0]}")
                    print(f"   Type of X: {type(points[0][0])}")
        except Exception as e:
            print(f"Error: {e}")

    # 2. Gantt Widget
    w_gantt = Widget.objects.filter(title__contains="Gantt").last()
    if w_gantt:
        print(f"\n[GANTT] {w_gantt.title}")
        try:
            data = WidgetDataService.get_widget_data(w_gantt, params)
            segments = data.get('data', [])
            print(f"Segments Count: {len(segments)}")
            if len(segments) > 0:
                print(f"   Sample Segment: {segments[0]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_response()
