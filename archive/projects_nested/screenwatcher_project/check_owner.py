import django
import os
import sys

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Dashboard
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    dashboard_id = "3443b17e-3e5f-4d92-8497-d94b5abdb3cb"
    dashboard = Dashboard.objects.get(id=dashboard_id)
    print(f"Dashboard: {dashboard.name}")
    print(f"Owner: {dashboard.user.username} (ID: {dashboard.user.id})")
    
    print("\n--- All Users ---")
    for u in User.objects.all():
        print(f"User: {u.username} (ID: {u.id})")

except Dashboard.DoesNotExist:
    print(f"Dashboard with ID {dashboard_id} not found.")
