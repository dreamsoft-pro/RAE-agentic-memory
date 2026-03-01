import os
import django
import sys

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard, Widget, WidgetSeries
from apps.telemetry.models import MetricDefinition

def check_and_update():
    dashboard_id = '1f537912-f1a3-4b6d-a4a0-75c3d4ac2df0'
    try:
        d = Dashboard.objects.get(id=dashboard_id)
        w = d.widgets.filter(title="Performance Metrics").first()
        
        if not w:
            print("Widget 'Performance Metrics' not found!")
            return
            
        print(f"Widget: {w.title} (ID: {w.id})")
        print(f"Current Config Range: {w.config.get('customStart')}")
        
        print("Series:")
        for s in w.series.all():
            print(f" - Metric: {s.metric.name} ({s.metric.code}) | Key: {s.metric.json_key} | Machine: {s.machine.code}")

        # Update Range to cover the imported data (Starts ~10:26)
        # Setting range to 10:00 - 23:00 on Jan 9th
        w.config['customStart'] = '2026-01-09 10:00:00'
        w.config['customEnd'] = '2026-01-09 23:00:00'
        w.save()
        print("\nUpdated Widget Range to 10:00 - 23:00 to include new data.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_and_update()
