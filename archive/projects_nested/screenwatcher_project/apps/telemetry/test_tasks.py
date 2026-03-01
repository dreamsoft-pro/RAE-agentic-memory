import pytest
from django.utils import timezone
from apps.registry.models import Machine, Line, Department, Factory
from apps.telemetry.models import TelemetryPoint, TelemetryHourlyRollup
from apps.telemetry.tasks import perform_hourly_rollup_task
import datetime

@pytest.fixture
def machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M1", line=l)

@pytest.mark.django_db
class TestTelemetryRollup:
    
    def test_hourly_rollup_task(self, machine):
        # 1. Setup raw data for a specific hour
        start_hour = timezone.now().replace(minute=0, second=0, microsecond=0) - datetime.timedelta(hours=2)
        
        # 3 points for 'temp'
        TelemetryPoint.objects.create(machine=machine, kind='temp', timestamp=start_hour + datetime.timedelta(minutes=10), payload=20.0)
        TelemetryPoint.objects.create(machine=machine, kind='temp', timestamp=start_hour + datetime.timedelta(minutes=20), payload=30.0)
        TelemetryPoint.objects.create(machine=machine, kind='temp', timestamp=start_hour + datetime.timedelta(minutes=30), payload=40.0)
        
        # 2 points for 'pressure' using dict format
        TelemetryPoint.objects.create(machine=machine, kind='pressure', timestamp=start_hour + datetime.timedelta(minutes=5), payload={'value': 1.0})
        TelemetryPoint.objects.create(machine=machine, kind='pressure', timestamp=start_hour + datetime.timedelta(minutes=15), payload={'value': 2.0})
        
        # 2. Run task
        result = perform_hourly_rollup_task(hour_str=start_hour.isoformat())
        assert "Hourly rollup completed" in result
        
        # 3. Verify rollups
        assert TelemetryHourlyRollup.objects.count() == 2
        
        temp_rollup = TelemetryHourlyRollup.objects.get(kind='temp')
        assert temp_rollup.min_value == 20.0
        assert temp_rollup.max_value == 40.0
        assert temp_rollup.avg_value == 30.0
        assert temp_rollup.count_points == 3
        
        press_rollup = TelemetryHourlyRollup.objects.get(kind='pressure')
        assert press_rollup.sum_value == 3.0
        assert press_rollup.count_points == 2

    def test_multi_metric_aggregation(self, machine):
        """Test for Iteration 10+: Aggregating many metrics into metrics_summary JSON."""
        from apps.telemetry.tasks import perform_hourly_rollup_task
        from apps.telemetry.models import MetricDefinition
        
        start_hour = timezone.now().replace(minute=0, second=0, microsecond=0) - datetime.timedelta(hours=5)
        
        # Define some metrics
        MetricDefinition.objects.create(code="ink_drops", json_key="ink", aggregation="sum")
        MetricDefinition.objects.create(code="avg_speed", json_key="speed", aggregation="avg")
        
        # Telemetry packets with multiple metrics
        TelemetryPoint.objects.create(
            machine=machine, kind='telemetry_packet', timestamp=start_hour + datetime.timedelta(minutes=1),
            payload={"ink": 100, "speed": 10}
        )
        TelemetryPoint.objects.create(
            machine=machine, kind='telemetry_packet', timestamp=start_hour + datetime.timedelta(minutes=5),
            payload={"ink": 200, "speed": 20}
        )
        
        perform_hourly_rollup_task(hour_str=start_hour.isoformat())
        
        rollup = TelemetryHourlyRollup.objects.get(machine=machine, kind='general_metrics')
        # print(rollup.metrics_summary)
        assert rollup.metrics_summary.get("ink_drops") == 300 # 100 + 200
        assert rollup.metrics_summary.get("avg_speed") == 15 # (10 + 20) / 2

