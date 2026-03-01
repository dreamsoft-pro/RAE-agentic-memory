
import os
import django
import sys
from django.utils import timezone

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard, Widget, WidgetSeries
from apps.registry.models import Machine
from apps.telemetry.models import MetricDefinition

def create_debug_dashboard():
    machine_code = 'TJ02'
    try:
        machine = Machine.objects.get(code=machine_code)
    except:
        print("Machine not found")
        return

    # Create Dashboard
    d, created = Dashboard.objects.get_or_create(
        name="DEBUG: Jan 19 Data Check",
        defaults={'user_id': 1} # Assuming admin user exists
    )
    
    # Clear widgets
    d.widgets.all().delete()
    
    print(f"Created Dashboard: {d.name} (ID: {d.id})")
    
    # Range covering exactly the data we found + margins
    # Data: 14:09 - 14:38 UTC.
    # Let's verify what '08:00' corresponds to.
    # We will set wide UTC range: 13:00 to 15:00.
    
    start_str = '2026-01-19T13:00'
    end_str = '2026-01-19T15:00'

    # Widget 1: Speed (Line)
    w = Widget.objects.create(
        dashboard=d,
        title="Jan 19 Speed Detail",
        widget_type="multi_series_chart",
        width=12, height=6,
        config={
            'machine_id': str(machine.id),
            'range': 'custom',
            'customStart': start_str,
            'customEnd': end_str
        }
    )
    
    # Add Series
    m_speed = MetricDefinition.objects.get(code='speed_tj') # Or 'speed'
    
    WidgetSeries.objects.create(
        widget=w, metric=m_speed, machine=machine,
        label="Speed (m/h)", color="#00ff00", order=1
    )
    
    print(f"Created Debug Widget. Check URL: http://localhost:9000/dashboard/{d.id}/")

if __name__ == "__main__":
    create_debug_dashboard()
