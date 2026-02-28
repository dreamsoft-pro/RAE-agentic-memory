
import os
import django
import sys

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard
from apps.registry.models import Machine

def fix_debug_dashboard():
    dashboard_id = 'ba824884-4c3f-4e4b-a856-4735e3841ea2'
    
    # Set to FULL DAY to catch any timezone shift issues
    start_str = '2026-01-19T00:00:00'
    end_str = '2026-01-19T23:59:59'

    try:
        d = Dashboard.objects.get(id=dashboard_id)
        for w in d.widgets.all():
            w.config['range'] = 'custom'
            w.config['customStart'] = start_str
            w.config['customEnd'] = end_str
            w.save()
            print(f"Updated Debug Widget Range: {start_str} - {end_str}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_debug_dashboard()
