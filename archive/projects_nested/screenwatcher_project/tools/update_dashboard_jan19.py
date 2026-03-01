
import os
import django
import sys

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard, Widget
from apps.registry.models import Machine

def update_widgets():
    dashboard_id = 'eb07f0f9-f65f-4298-a50d-fce6d00aebb0'
    
    # Updated range to include BOTH Jan 9 and Jan 19 data
    start_str = '2026-01-09T08:00' 
    end_str = '2026-01-19T15:00' 

    target_machine_code = 'TJ02'
    
    try:
        machine = Machine.objects.get(code=target_machine_code)
        d = Dashboard.objects.get(id=dashboard_id)
        print(f"Updating Dashboard: {d.name} for Machine: {machine.name}")

        # Update specific widgets
        targets = ['Performance Metrics', 'Total Production', 'Machine Status', 'OI Indicator']
        
        for t in targets:
            # Find widgets loosely matching the title
            widgets = d.widgets.filter(title__icontains=t)
            for w in widgets:
                print(f"Updating widget: {w.title} ({w.widget_type})")
                
                # Fix Machine ID
                w.config['machine_id'] = str(machine.id)
                
                # Set Custom Range covering both events
                w.config['range'] = 'custom'
                w.config['customStart'] = start_str
                w.config['customEnd'] = end_str
                
                # Ensure axis config exists for multi_series_chart
                if w.widget_type == 'multi_series_chart' and 'yAxis' not in w.config:
                     w.config['yAxis'] = [
                        {'type': 'value', 'name': 'Speed (m/h)', 'position': 'left'},
                        {'type': 'value', 'name': 'Area (m2)', 'position': 'right'}
                     ]

                w.save()
                print(f" - Config updated: Machine={w.config['machine_id']}, Range={start_str} -> {end_str}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_widgets()
