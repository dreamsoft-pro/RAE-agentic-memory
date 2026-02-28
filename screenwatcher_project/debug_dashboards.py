
import django
import os
import sys

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Dashboard, Widget, WidgetSeries
from apps.registry.models import Machine
from apps.telemetry.models import MetricDefinition

dashboards = Dashboard.objects.all()

for d in dashboards:
    print(f"\nDashboard: {d.name} (ID: {d.id}) - Default: {d.is_default}")
    widgets = d.widgets.all()
    if not widgets:
        print("  [WARNING] No widgets found.")
        continue
    
    for w in widgets:
        print(f"  Widget: {w.title} (Type: {w.widget_type})")
        series = w.series.all()
        # Some widgets might use 'config' instead of 'series'
        print(f"    Config: {w.config}")
        
        if series.exists():
            for s in series:
                metric_name = s.metric.name if s.metric else "None"
                machine_name = s.machine.name if s.machine else "None"
                print(f"    - Series Label: {s.label}, Metric: {metric_name} (Machine: {machine_name})")
        else:
            print("    [INFO] No explicit WidgetSeries found (might rely on config).")
