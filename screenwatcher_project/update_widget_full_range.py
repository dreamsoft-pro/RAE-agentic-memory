
import os
import django
import sys
from datetime import datetime
from django.utils import timezone

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard, Widget

def update_widgets():
    dashboard_id = '1f537912-f1a3-4b6d-a4a0-75c3d4ac2df0'
    start_str = '2026-01-09 10:00:00'
    end_str = '2026-01-16 15:00:00'
    
    try:
        d = Dashboard.objects.get(id=dashboard_id)
        print(f"Updating Dashboard: {d.name}")

        # Update specific widgets
        targets = ['Performance Metrics', 'Total Production (m2)']
        
        for t in targets:
            w = d.widgets.filter(title__icontains=t).first()
            if w:
                w.config['range'] = 'custom'
                w.config['customStart'] = start_str
                w.config['customEnd'] = end_str
                w.save()
                print(f" - Updated '{w.title}' to range: {start_str} -> {end_str}")
            else:
                print(f" - Warning: Widget matching '{t}' not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_widgets()
