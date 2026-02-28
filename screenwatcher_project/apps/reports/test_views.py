import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.registry.models import Machine, Line, Department, Factory
from apps.oee.models import DailyOEE
import datetime

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_user(db):
    return User.objects.create_user(username="reporter", password="password", is_superuser=True)

@pytest.fixture
def sample_oee(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    m = Machine.objects.create(name="M1", code="M1", line=l)
    return DailyOEE.objects.create(
        machine=m, 
        date=datetime.date.today(),
        availability=80.0,
        performance=90.0,
        quality=100.0,
        oee=72.0
    )

@pytest.mark.django_db
class TestReportsAPI:
    def test_export_oee_csv(self, api_client, auth_user, sample_oee):
        api_client.force_authenticate(user=auth_user)
        url = reverse('export-oee')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'
        content = response.content.decode('utf-8')
        assert 'M1' in content
        assert '80.00' in content

    def test_export_events_csv(self, api_client, auth_user):
        api_client.force_authenticate(user=auth_user)
        url = reverse('export-events')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'
