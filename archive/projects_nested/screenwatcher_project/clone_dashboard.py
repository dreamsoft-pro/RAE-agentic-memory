import os
import django
import sys
import uuid
from django.db import transaction

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard, Widget, WidgetSeries

def clone_dashboard():
    original_id = 'eb07f0f9-f65f-4298-a50d-fce6d00aebb0'
    
    try:
        original = Dashboard.objects.get(id=original_id)
    except Dashboard.DoesNotExist:
        print(f"Error: Dashboard {original_id} not found.")
        return

    new_uuid = uuid.uuid4()
    new_name = f"{original.name} (V5 CLONE)"
    
    print(f"Cloning '{original.name}'...")

    with transaction.atomic():
        # 1. Clone Dashboard
        new_dashboard = Dashboard.objects.create(
            id=new_uuid,
            user=original.user,
            name=new_name,
            is_public=original.is_public,
            is_default=False # Don't make clone default
        )

        # 2. Clone Widgets
        for w in original.widgets.all():
            new_widget = Widget.objects.create(
                dashboard=new_dashboard,
                title=w.title,
                widget_type=w.widget_type,
                config=w.config,
                pos_x=w.pos_x,
                pos_y=w.pos_y,
                width=w.width,
                height=w.height
            )

            # 3. Clone Series (if any)
            for s in w.series.all():
                WidgetSeries.objects.create(
                    widget=new_widget,
                    metric=s.metric,
                    machine=s.machine,
                    label=s.label,
                    y_axis=s.y_axis,
                    chart_type=s.chart_type,
                    color=s.color,
                    order=s.order
                )

    print(f"\nSUCCESS! Dashboard cloned.")
    print(f"Original ID: {original.id}")
    print(f"New ID:      {new_dashboard.id}")
    print(f"New URL:     http://localhost:9000/dashboard/{new_dashboard.id}/")

if __name__ == "__main__":
    clone_dashboard()
