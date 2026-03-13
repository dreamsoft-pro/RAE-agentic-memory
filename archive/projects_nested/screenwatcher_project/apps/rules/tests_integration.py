import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.registry.models import Machine, Line, Department, Factory
from apps.rules.models import Rule, RuleHit
from apps.telemetry.models import TelemetryPoint

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M-TEST-RULE", line=l)

@pytest.mark.django_db
class TestReactiveRules:
    
    def test_end_to_end_rule_trigger(self, api_client, machine):
        # 1. Setup Rule
        logic = {">": [{"var": "temp"}, 100]}
        actions = [{"type": "log", "level": "error", "message": "Overheat on {machine_code}!"}]
        
        rule = Rule.objects.create(
            name="Temp Alert",
            logic=logic,
            actions=actions,
            is_active=True
        )
        
        # 2. Ingest Data (via Collector API)
        url = reverse('collector-ingest')
        payload = {
            "machine_code": machine.code,
            "metrics": {
                "temp": 120, # Should trigger
                "status": "RUN"
            }
        }
        
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # 3. Verify RuleHit
        assert RuleHit.objects.count() == 1
        hit = RuleHit.objects.first()
        assert hit.rule == rule
        assert hit.machine == machine
        assert hit.payload['temp'] == 120
        
        # 4. Verify Action Log
        assert len(hit.action_log) == 1
        assert hit.action_log[0]['type'] == 'log'
        assert hit.action_log[0]['status'] == 'executed'

    def test_rule_not_triggered(self, api_client, machine):
        # Setup Rule
        logic = {">": [{"var": "temp"}, 100]}
        Rule.objects.create(name="Temp Alert", logic=logic, actions=[])
        
        # Ingest Safe Data
        url = reverse('collector-ingest')
        payload = {
            "machine_code": machine.code,
            "metrics": {"temp": 90}
        }
        
        api_client.post(url, payload, format='json')
        
        # Verify NO Hit
        assert RuleHit.objects.count() == 0
