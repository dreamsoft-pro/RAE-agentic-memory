import pytest
from django.utils import timezone
from apps.registry.models import Machine, Line, Department, Factory
from apps.telemetry.models import TelemetryPoint
from apps.oee.models import DailyOEE
from apps.oee.tasks import calculate_daily_oee_task, calculate_all_machines_oee_task
import datetime

@pytest.fixture
def machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M1", line=l, cycle_time_ideal=60)

@pytest.mark.django_db
class TestOEETasks:
    
    def test_calculate_daily_oee_task(self, machine):
        now = timezone.now()
        date = now.date()
        date_str = date.isoformat()
        
        # Create telemetry
        TelemetryPoint.objects.create(
            machine=machine,
            timestamp=now,
            kind='raw',
            payload={"status": "RUNNING", "parts_delta": 10, "good_parts_delta": 10}
        )
        
        # Run task synchronously (eager mode handled by settings_test.py)
        result = calculate_daily_oee_task(str(machine.id), date_str)
        
        assert "OEE calculated" in result
        assert DailyOEE.objects.count() == 1
        assert DailyOEE.objects.get().total_parts == 10

    def test_calculate_all_machines_oee_task(self, machine):
        from unittest.mock import patch
        # Create another machine
        m2 = Machine.objects.create(name="M2", code="M2", line=machine.line)
        
        # Run task
        with patch('apps.oee.tasks.calculate_daily_oee_task.delay') as mock_delay:
            result = calculate_all_machines_oee_task()
            assert "Triggered OEE calculation for 2 machines" in result
            assert mock_delay.call_count == 2
