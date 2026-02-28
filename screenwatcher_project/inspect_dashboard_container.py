
import os
import django
import sys

# In-container path is /app
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard, Widget

def inspect():
    dashboard_id = '1f537912-f1a3-4b6d-a4a0-75c3d4ac2df0'
    try:
        d = Dashboard.objects.get(id=dashboard_id)
        print(f"DASHBOARD: {d.name}")
        for w in d.widgets.all():
            print(f"  WIDGET: {w.title} | TYPE: {w.widget_type} | CONFIG: {w.config}")
    except Exception as e:
        print(f"Error: {e}")
        print("Listing all dashboards:")
        for d in Dashboard.objects.all():
            print(f" - {d.name} ({d.id})")

if __name__ == "__main__":
    inspect()
