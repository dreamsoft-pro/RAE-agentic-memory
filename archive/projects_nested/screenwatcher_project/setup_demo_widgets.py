
import os
import sys
import django

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Widget, WidgetSeries, Dashboard
from apps.telemetry.models import MetricDefinition
from apps.registry.models import Machine

def setup_demo():
    print("Setting up Demo Multi-Series Chart...")
    
    # 1. Ensure Metrics exist
    m_speed, _ = MetricDefinition.objects.get_or_create(code='speed', defaults={'name': 'Speed', 'unit': 'ppm', 'json_key': 'speed', 'aggregation': 'avg'})
    m_temp, _ = MetricDefinition.objects.get_or_create(code='temp', defaults={'name': 'Temperature', 'unit': '°C', 'json_key': 'temp', 'aggregation': 'avg'})
    m_pressure, _ = MetricDefinition.objects.get_or_create(code='pressure', defaults={'name': 'Pressure', 'unit': 'bar', 'json_key': 'pressure', 'aggregation': 'avg'})
    
    print("Metrics ready.")

    # 2. Get Machine (TM01)
    try:
        machine = Machine.objects.get(code='TM01')
    except Machine.DoesNotExist:
        print("Machine TM01 not found! Ensure simulator/seed ran.")
        return

    # 3. Find or Create the Custom Chart Widget
    # We look for the one with specific ID from logs, or create new one on Main Dashboard
    target_id = '89ec0304-4202-417c-8f67-3c469fcae13a'
    widget = Widget.objects.filter(id=target_id).first()
    
    if not widget:
        print(f"Widget {target_id} not found. Creating new on default dashboard.")
        dashboard = Dashboard.objects.filter(is_default=True).first()
        if not dashboard:
            print("No default dashboard found.")
            return
            
        widget = Widget.objects.create(
            dashboard=dashboard,
            title="Demo Multi-Signal Chart",
            widget_type="multi_series_chart",
            width=8, height=6, pos_x=0, pos_y=10,
            config={"range": "24h"}
        )
    else:
        print(f"Found existing widget: {widget.title}")
        widget.title = "Demo Multi-Signal Chart"
        widget.config = {"range": "24h"}
        widget.save()

    # 4. Configure Series
    # Clear existing series for this widget to avoid duplicates
    widget.series.all().delete()
    
    # Series 1: Speed (Left Axis, Blue)
    WidgetSeries.objects.create(
        widget=widget,
        metric=m_speed,
        machine=machine,
        label="Line Speed",
        y_axis="left",
        chart_type="line",
        color="#5470c6",
        order=1
    )
    
    # Series 2: Temperature (Right Axis, Red)
    WidgetSeries.objects.create(
        widget=widget,
        metric=m_temp,
        machine=machine,
        label="Core Temp",
        y_axis="right",
        chart_type="line",
        color="#ee6666",
        order=2
    )
    
    # Series 3: Pressure (Right Axis, Green)
    WidgetSeries.objects.create(
        widget=widget,
        metric=m_pressure,
        machine=machine,
        label="Hydraulic Pressure",
        y_axis="right",
        chart_type="line",
        color="#91cc75",
        order=3
    )
    
    print("Widget Series configured successfully.")
    print(f"Widget ID: {widget.id}")

if __name__ == "__main__":
    setup_demo()
