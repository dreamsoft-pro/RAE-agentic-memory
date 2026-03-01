import os
import django
import sys

sys.path.append('/home/grzegorz-lesniowski/cloud/screenwatcher_project')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.services.widget_data import WidgetDataService
from apps.dashboards.models import Widget, Dashboard
from apps.dashboards.serializers import WidgetSerializer

print("✅ Imports successful")

# Check if we can instantiate providers
print(f"Providers: {WidgetDataService.PROVIDERS.keys()}")

# Dry run test (mock widget)
try:
    # Create dummy widget in memory
    w = Widget(widget_type='oee_gauge', config={'machine_id': 1})
    provider = WidgetDataService.PROVIDERS['oee_gauge']()
    
    # Check new providers
    gantt = WidgetDataService.PROVIDERS['machine_gantt']()
    heatmap = WidgetDataService.PROVIDERS['oee_heatmap']()
    
    print("✅ Provider instantiation successful")
except Exception as e:
    print(f"❌ Error: {e}")
