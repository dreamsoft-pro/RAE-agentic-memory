import os
import sys
import django
import json

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Widget
from apps.dashboards.services.widget_data import WidgetDataService

def debug():
    print("--- DEBUGGING GANTT & AREA ---")
    
    # 1. Inspect Gantt Widget
    w_gantt = Widget.objects.filter(title="Oś Czasu (Gantt)").last()
    if w_gantt:
        print(f"\nGANTT Widget: {w_gantt.id}")
        data = WidgetDataService.get_widget_data(w_gantt, None)
        segments = data.get('data', [])
        print(f"Total Segments: {len(segments)}")
        
        # Analyze statuses
        statuses = {}
        for s in segments:
            name = s.get('name')
            statuses[name] = statuses.get(name, 0) + 1
            
        print("Status Distribution:", statuses)
        if segments:
            print("Sample Segment:", segments[0])
    else:
        print("Gantt Widget NOT FOUND")

    # 2. Inspect Chart Widget Area Series
    w_chart = Widget.objects.filter(title__contains="Wydajność Maszyny").last()
    if w_chart:
        print(f"\nCHART Widget: {w_chart.id}")
        data = WidgetDataService.get_widget_data(w_chart, None)
        series = data.get('series', [])
        for s in series:
            if 'Powierzchnia' in s.get('name', ''):
                points = s.get('data', [])
                non_zero = [p for p in points if p[1] > 0]
                print(f"Series '{s.get('name')}': {len(points)} points. Non-zero: {len(non_zero)}")
                if non_zero:
                    print(f"Sample Non-Zero: {non_zero[0]}")

if __name__ == "__main__":
    debug()
