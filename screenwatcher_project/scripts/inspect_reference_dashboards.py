
import os
import sys
import django
import json
from uuid import UUID

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Dashboard, Widget, WidgetSeries

PARAMS = [
    '563e3ad2-5330-4618-b427-7600e34fccfc',
    'eb07f0f9-f65f-4298-a50d-fce6d00aebb0'
]

def inspect():
    for d_id in PARAMS:
        print(f"\n=== DASHBOARD {d_id} ===")
        try:
            dash = Dashboard.objects.get(id=d_id)
            print(f"Name: {dash.name}")
            print(f"User: {dash.user}")
            
            widgets = dash.widgets.all()
            for w in widgets:
                print(f"  [Widget ID: {w.id}]")
                print(f"  Title: {w.title}")
                print(f"  Type: {w.widget_type}")
                print(f"  Config: {json.dumps(w.config, indent=2)}")
                
                if w.widget_type == 'multi_series_chart':
                    series = w.series.all()
                    for s in series:
                        print(f"    - Series: {s.label} | Metric: {s.metric.code} | Key: {s.metric.json_key}")
        except Dashboard.DoesNotExist:
            print("  NOT FOUND")
        except Exception as e:
            print(f"  ERROR: {e}")

if __name__ == "__main__":
    inspect()
