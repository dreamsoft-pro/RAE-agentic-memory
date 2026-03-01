import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.registry.models import Machine, Line, Department, Factory
from apps.operator_panel.models import Operator, ReasonCode

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_user(db):
    return User.objects.create_user(username="admin", password="password", is_superuser=True)

@pytest.fixture
def setup_machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M1", line=l)

@pytest.mark.django_db
class TestOperatorPanelAPI:
    def test_operator_crud(self, api_client, auth_user, setup_machine):
        api_client.force_authenticate(user=auth_user)
        
        # Create
        url = reverse('operator-list')
        user2 = User.objects.create_user(username="op1", password="password")
        data = {
            "user": user2.id,
            "badge_id": "B001",
            "default_machine": setup_machine.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # List
        response = api_client.get(url)
        assert len(response.data) == 1
        assert response.data[0]['badge_id'] == "B001"

    def test_reason_code_api(self, api_client, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('reasoncode-list')
        
        data = {
            "code": "M01",
            "description": "Mechanical Failure",
            "category": "Maintenance",
            "severity": "CRITICAL"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify
        assert ReasonCode.objects.filter(code="M01").exists()
