import pytest
from django.utils import timezone
from apps.registry.models import Machine, Line, Department, Factory
from apps.telemetry.models import TelemetryPoint
from apps.oee.models import DailyOEE
from apps.oee.services import OEECalculator
import datetime

@pytest.fixture
def machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M1", line=l, cycle_time_ideal=60) # 60s ideal

@pytest.mark.django_db
class TestOEECalculation:
    
    def test_basic_calculation(self, machine):
        now = datetime.datetime(2025, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
        date = timezone.localdate(now)
        
        # 1. Create Telemetry Points (Simulate 10 minutes of running)
        for i in range(10):
            t = now + datetime.timedelta(minutes=i)
            TelemetryPoint.objects.create(
                machine=machine,
                timestamp=t,
                kind='raw',
                payload={"status": "RUNNING", "parts_delta": 1, "good_parts_delta": 1}
            )
            
        # 2. Run Calculator
        oee_record = OEECalculator.calculate_daily(machine, date)
        
        # 3. Verify
        # Run Time: 10 mins
        # Total Parts: 10
        # Good Parts: 10
        # Availability: 10 / 1440 * 100 = 0.69%
        # Performance: Ideal = 10 mins * (60s / 60s) = 10 parts. Actual = 10. Perf = 100%.
        # Quality: 10/10 = 100%.
        
        assert oee_record.run_time_min == 10
        assert oee_record.total_parts == 10
        assert oee_record.good_parts == 10
        
        assert oee_record.performance == 100.0
        assert oee_record.quality == 100.0
        # Availability is small because we assume 24h day
        expected_avail = (10 / 1440) * 100
        assert abs(oee_record.availability - expected_avail) < 0.01

    def test_quality_drop(self, machine):
        now = datetime.datetime(2025, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
        date = timezone.localdate(now)
        
        # 1. Create Telemetry: 10 parts, but only 5 good
        TelemetryPoint.objects.create(
             machine=machine,
             timestamp=now,
             kind='raw',
             payload={"status": "RUNNING", "parts_delta": 10, "good_parts_delta": 5}
        )
        
        # 2. Run Calculator
        oee_record = OEECalculator.calculate_daily(machine, date)
        
        # 3. Verify
        assert oee_record.total_parts == 10
        assert oee_record.good_parts == 5
        assert oee_record.quality == 50.0 # 5/10

@pytest.mark.django_db
class TestOEEMetrics:
    def test_mtbf_mttr_calculation(self, machine):
        from apps.oee.services import OEEMetricsService
        from apps.oee.models import DowntimeEvent
        from apps.operator_panel.models import ReasonCode
        
        start = timezone.now() - datetime.timedelta(hours=10)
        end = timezone.now()
        
        maint_reason = ReasonCode.objects.create(code='MAINTENANCE', description='Maintenance')
        
        # Simulate 2 downtimes
        # 1. 30 min (Maintenance)
        DowntimeEvent.objects.create(
            machine=machine, start_time=start, end_time=start + datetime.timedelta(minutes=30),
            duration_seconds=1800, reason=maint_reason
        )
        # 2. 10 min (Failure)
        DowntimeEvent.objects.create(
            machine=machine, start_time=start + datetime.timedelta(hours=2), 
            end_time=start + datetime.timedelta(hours=2, minutes=10),
            duration_seconds=600
        )
        
        # MTTR (Maintenance only): Total 30m / 1 event = 30m
        mttr = OEEMetricsService.calculate_mttr(machine, start, end)
        assert mttr == 30.0
        
        # MTBF (Total operating time / Failure events)
        # Total time = 10h. Total downtime = 40m. Operating = 9h 20m = 9.33h
        # Failure count = 1. MTBF = 9.33h
        mtbf = OEEMetricsService.calculate_mtbf(machine, start, end)
        assert mtbf > 9.0