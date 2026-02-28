import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.registry.models import Machine, Line, Department, Factory
from apps.telemetry.models import TelemetryPoint

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M-TEST-01", line=l)

@pytest.fixture
def auth_user(db):
    from django.contrib.auth.models import User
    return User.objects.create_user(username="agent", password="password")

@pytest.mark.django_db
class TestCollectorAPI:
    def test_ingest_success(self, api_client, machine, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('collector-ingest')
        payload = {
            "machine_code": machine.code,
            "metrics": {
                "status": "RUNNING",
                "temp": 80.5
            }
        }
        
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify DB
        assert TelemetryPoint.objects.count() == 1
        tp = TelemetryPoint.objects.first()
        assert tp.machine == machine
        assert tp.payload['status'] == "RUNNING"
        assert tp.kind == "telemetry_packet"

    def test_ingest_unknown_machine(self, api_client, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('collector-ingest')
        payload = {
            "machine_code": "UNKNOWN-999",
            "metrics": {"val": 1}
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_ingest_invalid_payload(self, api_client, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('collector-ingest')
        payload = {"foo": "bar"} # Missing required fields
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_ingest_with_legacy_config(self, api_client, machine, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('collector-ingest')
        payload = {
            "machine_code": machine.code,
            "metrics": {"status": "OK"},
            "legacy_config": {
                "host": "10.0.0.50",
                "database": "prod_db",
                "user": "edge_user",
                "password": "secret_password"
            }
        }
        
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify connection profile created
        from apps.legacy_integration.models import ConnectionProfile
        profile = ConnectionProfile.objects.get(name=f"EdgeConfig_{machine.code}")
        assert profile.host == "10.0.0.50"
        assert profile.database == "prod_db"
        
        # Verify machine linked
        machine.refresh_from_db()
        assert machine.legacy_connection == profile

    def test_ingest_triggers_rules(self, api_client, machine, auth_user):
        from apps.rules.models import Rule, RuleHit
        api_client.force_authenticate(user=auth_user)
        
        # 1. Setup a rule
        Rule.objects.create(
            name="Critical Temp",
            logic={">": [{"var": "temp"}, 90]},
            actions=[{"type": "log", "message": "CRITICAL TEMP!"}]
        )
        
        # 2. Ingest matching data
        url = reverse('collector-ingest')
        payload = {
            "machine_code": machine.code,
            "metrics": {"temp": 95}
        }
        response = api_client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # 3. Verify RuleHit
        assert RuleHit.objects.count() == 1
        hit = RuleHit.objects.first()
        assert hit.rule.name == "Critical Temp"
        assert hit.payload['temp'] == 95