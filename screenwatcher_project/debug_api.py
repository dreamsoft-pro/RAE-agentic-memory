
import os
import sys
import django

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from apps.dashboards.views import WidgetDataAPI
from apps.dashboards.models import Widget
from django.contrib.auth import get_user_model

def test_api():
    factory = APIRequestFactory()
    User = get_user_model()
    
    try:
        # Get admin user
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            print("No superuser found!")
            return

        # Find the Multi-Series Widget created by setup script
        widget = Widget.objects.filter(title="Demo Multi-Signal Chart").first()
        if not widget:
            print("Demo widget not found!")
            return

        print(f"Testing WidgetDataAPI for: {widget.title} ({widget.id})")
        
        # Simulate request
        request = factory.get(f'/dashboard/api/widgets/{widget.id}/data/')
        force_authenticate(request, user=admin)
        
        # Instantiate view
        view = WidgetDataAPI.as_view()
        
        # Run view
        response = view(request, pk=widget.id)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            series = response.data.get('series', [])
            print(f"Series Count: {len(series)}")
            for s in series:
                print(f" - Series: {s['name']}, Points: {len(s['data'])}")
        else:
            print(f"Data: {response.data}")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api()
