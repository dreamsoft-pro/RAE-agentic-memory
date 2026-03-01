import pytest
from rest_framework.test import APIClient
from django.utils import timezone
from apps.registry.models import Machine, Factory, Department, Line
from apps.oee.models import DowntimeEvent
from apps.operator_panel.models import ReasonCode
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='op', password='password')

@pytest.fixture
def machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M1", line=l)

@pytest.fixture
def reason_code(db):
    return ReasonCode.objects.create(code="ERR01", description="Mechanical Failure")

@pytest.mark.django_db
def test_assign_reason_code(api_client, user, machine, reason_code):
    api_client.force_authenticate(user=user)
    
    # Create Event
    event = DowntimeEvent.objects.create(
        machine=machine,
        start_time=timezone.now(),
        duration_seconds=60
    )
    
    url = f"/api/oee/downtime-events/{event.id}/"
    payload = {
        "reason_code": "ERR01",
        "comment": "Fixed by reset"
    }
    
    response = api_client.patch(url, payload)
    
    assert response.status_code == 200
    event.refresh_from_db()
    assert event.reason == reason_code
    assert event.comment == "Fixed by reset"

@pytest.mark.django_db
def test_filter_uncategorized(api_client, user, machine, reason_code):
    api_client.force_authenticate(user=user)
    
    # Create 2 events: one with reason, one without
    e1 = DowntimeEvent.objects.create(machine=machine, start_time=timezone.now(), reason=reason_code)
    e2 = DowntimeEvent.objects.create(machine=machine, start_time=timezone.now())
    
    url = "/api/oee/downtime-events/?uncategorized=true"
    response = api_client.get(url)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == str(e2.id)
