import os
import django
import uuid

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.registry.models import Machine
from apps.dashboards.models import Dashboard, Widget, WidgetSeries
from apps.telemetry.models import MetricDefinition
from django.contrib.auth.models import User

def setup():
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
    
    machine = Machine.objects.get(code='TJ02')
    dashboard, _ = Dashboard.objects.get_or_create(user=user, is_default=True, defaults={'name': 'Main Dashboard'})
    
    # Ensure metric definitions exist
    speed_metric, _ = MetricDefinition.objects.get_or_create(
        code='speed_m2h',
        defaults={'name': 'Speed (m2/h)', 'unit': 'm2/h', 'json_key': 'metrics.pole_5'}
    )
    area_metric, _ = MetricDefinition.objects.get_or_create(
        code='area_m2',
        defaults={'name': 'Area (m2)', 'unit': 'm2', 'json_key': 'metrics.pole_2'}
    )

    # 1. Multi-Series Chart Widget
    widget, created = Widget.objects.get_or_create(
        dashboard=dashboard,
        widget_type='multi_series_chart',
        title='TrueJet2 Performance',
        defaults={
            'config': {
                'machine_id': str(machine.id),
                'customStart': '2026-01-21T00:00:00Z',
                'customEnd': '2026-01-21T23:59:59Z'
            },
            'width': 12,
            'height': 6
        }
    )
    
    WidgetSeries.objects.get_or_create(
        widget=widget,
        metric=speed_metric,
        machine=machine,
        defaults={'label': 'Prędkość (m2/h)', 'chart_type': 'line', 'color': '#5470c6'}
    )
    
    # 2. Machine Gantt Widget
    Widget.objects.get_or_create(
        dashboard=dashboard,
        widget_type='machine_gantt',
        title='TJ02 Timeline',
        defaults={
            'config': {
                'machine_id': str(machine.id),
                'customStart': '2026-01-21T00:00:00Z',
                'customEnd': '2026-01-21T23:59:59Z'
            },
            'width': 12,
            'height': 4
        }
    )

    print(f"Setup complete. Widget ID for Multi-Series: {widget.id}")

if __name__ == "__main__":
    setup()
