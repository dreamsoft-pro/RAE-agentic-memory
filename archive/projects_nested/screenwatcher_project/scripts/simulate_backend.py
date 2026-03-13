
import os
import sys
import django
import json

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Widget
from apps.dashboards.services.widget_data import WidgetDataService

def simulate():
    print("--- SIMULATING BACKEND DATA FETCH ---")
    
    # 1. Find the Chart Widget
    w = Widget.objects.filter(title__contains="Wydajność Maszyny", widget_type="multi_series_chart").last()
    if not w:
        print("Widget not found!")
        return

    print(f"Widget: {w.title} (ID: {w.id})")
    print(f"Config: {json.dumps(w.config, indent=2)}")
    
    # 2. Call Service (Simulate Frontend Request without params -> should use config dates)
    print("\nCalling get_widget_data(widget, params=None)...")
    try:
        data = WidgetDataService.get_widget_data(w, None)
        
        # 3. Analyze Response
        series = data.get('series', [])
        print(f"Returned Series Count: {len(series)}")
        
        for s in series:
            name = s.get('name')
            points = s.get('data', [])
            count = len(points)
            print(f" - Series '{name}': {count} points")
            if count > 0:
                print(f"   First: {points[0]}")
                print(f"   Last:  {points[-1]}")
            else:
                print("   [EMPTY]")
                
    except Exception as e:
        print(f"ERROR calling service: {e}")
        import traceback
        traceback.print_exc()

    # 4. Gantt Simulation
    print("\n--- GANTT SIMULATION ---")
    w_gantt = Widget.objects.filter(widget_type="machine_gantt").last()
    if w_gantt:
        print(f"Widget: {w_gantt.title}")
        try:
            data = WidgetDataService.get_widget_data(w_gantt, None)
            segments = data.get('data', [])
            print(f"Segments Count: {len(segments)}")
            if segments:
                print(f"First Segment: {segments[0]}")
        except Exception as e:
            print(f"Gantt Error: {e}")

if __name__ == "__main__":
    simulate()
