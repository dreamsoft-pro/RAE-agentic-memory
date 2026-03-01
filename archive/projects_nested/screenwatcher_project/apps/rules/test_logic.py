import pytest
from django.utils import timezone
from apps.registry.models import Machine, Line, Department, Factory
from apps.telemetry.models import TelemetryPoint
from apps.rules.models import Rule, RuleHit
from apps.rules.services import RuleEvaluator

@pytest.fixture
def setup_machine(db):
    factory = Factory.objects.create(name="Test Factory", code="TF01")
    department = Department.objects.create(name="Test Dept", code="TD01", factory=factory)
    line = Line.objects.create(name="Test Line", code="TL01", department=department)
    machine = Machine.objects.create(name="Test Machine", code="TM01", line=line)
    return machine

@pytest.mark.django_db
class TestRuleEvaluator:

    def test_process_telemetry_global_rule(self, setup_machine):
        machine = setup_machine
        # Global rule: temp > 100
        Rule.objects.create(
            name="High Temp Global",
            logic={">": [{"var": "temp"}, 100]},
            actions=[{"type": "log", "message": "Global Alert!"}]
        )
        
        # 1. Matches
        tp_match = TelemetryPoint.objects.create(
            machine=machine,
            kind="test",
            timestamp=timezone.now(),
            payload={"temp": 120}
        )
        hits = RuleEvaluator.process_telemetry(tp_match)
        assert len(hits) == 1
        assert hits[0].rule.name == "High Temp Global"
        assert RuleHit.objects.count() == 1

        # 2. No match
        tp_no_match = TelemetryPoint.objects.create(
            machine=machine,
            kind="test",
            timestamp=timezone.now(),
            payload={"temp": 80}
        )
        hits = RuleEvaluator.process_telemetry(tp_no_match)
        assert len(hits) == 0
        assert RuleHit.objects.count() == 1 # Still only the first one

    def test_process_telemetry_machine_specific_rule(self, setup_machine):
        machine = setup_machine
        other_factory = Factory.objects.create(name="Other Factory", code="OF01")
        other_dept = Department.objects.create(name="Other Dept", code="OD01", factory=other_factory)
        other_line = Line.objects.create(name="Other Line", code="OL01", department=other_dept)
        other_machine = Machine.objects.create(name="Other Machine", code="OM01", line=other_line)

        # Rule only for OM01
        Rule.objects.create(
            name="OM01 Special",
            machine=other_machine,
            logic={"==": [{"var": "status"}, "ERROR"]},
            actions=[]
        )

        # Telemetry from TM01 (setup_machine)
        tp_tm01 = TelemetryPoint.objects.create(
            machine=machine,
            kind="test",
            timestamp=timezone.now(),
            payload={"status": "ERROR"}
        )
        hits = RuleEvaluator.process_telemetry(tp_tm01)
        assert len(hits) == 0 # Rule is machine-specific

        # Telemetry from OM01
        tp_om01 = TelemetryPoint.objects.create(
            machine=other_machine,
            kind="test",
            timestamp=timezone.now(),
            payload={"status": "ERROR"}
        )
        hits = RuleEvaluator.process_telemetry(tp_om01)
        assert len(hits) == 1
        assert hits[0].rule.name == "OM01 Special"

    def test_action_execution_log(self, setup_machine, caplog):
        import logging
        machine = setup_machine
        Rule.objects.create(
            name="Alert Rule",
            logic={">": [{"var": "pressure"}, 50]},
            actions=[{"type": "log", "level": "error", "message": "High pressure on {machine_code}: {pressure}"}]
        )

        tp = TelemetryPoint.objects.create(
            machine=machine,
            kind="test",
            timestamp=timezone.now(),
            payload={"pressure": 65}
        )
        
        with caplog.at_level(logging.ERROR):
            RuleEvaluator.process_telemetry(tp)
            
        assert "High pressure on TM01: 65" in caplog.text

    def test_inactive_rule(self, setup_machine):
        machine = setup_machine
        Rule.objects.create(
            name="Inactive Rule",
            logic={"==": [{"var": "x"}, 1]},
            is_active=False,
            actions=[]
        )

        tp = TelemetryPoint.objects.create(
            machine=machine,
            kind="test",
            timestamp=timezone.now(),
            payload={"x": 1}
        )
        hits = RuleEvaluator.process_telemetry(tp)
        assert len(hits) == 0
