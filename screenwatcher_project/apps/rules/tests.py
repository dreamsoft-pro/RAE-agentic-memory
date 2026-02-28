import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from apps.rules.models import Rule
from apps.registry.models import Machine, Line, Department, Factory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_user(db):
    # User for simulation (just authenticated)
    return User.objects.create_user(username='tester', password='password')

@pytest.mark.django_db
class TestRulesEngine:
    
    def test_simulation_true(self, api_client, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('rule-simulate')
        
        # Logic: temp > 80
        logic = {">": [{"var": "temp"}, 80]}
        data = {"temp": 85}
        
        response = api_client.post(url, {"logic": logic, "data": data}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] is True

    def test_simulation_false(self, api_client, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('rule-simulate')
        
        # Logic: temp > 80
        logic = {">": [{"var": "temp"}, 80]}
        data = {"temp": 70}
        
        response = api_client.post(url, {"logic": logic, "data": data}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] is False

    def test_complex_logic(self, api_client, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('rule-simulate')
        
        # Logic: (temp > 80) AND (status == "RUNNING")
        logic = {
            "and": [
                {">": [{"var": "temp"}, 80]},
                {"==": [{"var": "status"}, "RUNNING"]}
            ]
        }
        data = {"temp": 90, "status": "RUNNING"}
        
        response = api_client.post(url, {"logic": logic, "data": data}, format='json')
        assert response.data['result'] is True
        
        # Fail case
        data_fail = {"temp": 90, "status": "STOPPED"}
        response = api_client.post(url, {"logic": logic, "data": data_fail}, format='json')
        assert response.data['result'] is False
