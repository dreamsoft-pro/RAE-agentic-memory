import os
import sys
sys.path.append('/app')
import django
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from apps.dashboards.views import TelemetrySeriesAPI
from apps.registry.models import Machine

factory = APIRequestFactory()
view = TelemetrySeriesAPI.as_view()

# Find TJ02
machine = Machine.objects.get(code='TJ02')
print(f"Testing API for Machine: {machine.code} ({machine.id})")

# Define request
url = f'/dashboard/api/series/?machine_id={machine.id}&metric=clean_speed&from=2026-01-21T00:00:00&to=2026-01-22T23:59:59'
request = factory.get(url)

# Execute
response = view(request)
data = response.data.get('data', [])

print(f"URL: {url}")
print(f"Status Code: {response.status_code}")
print(f"Data Points Returned: {len(data)}")

if data:
    print("First 3 points:")
    for p in data[:3]:
        print(p)
else:
    print("WARNING: No data returned!")
