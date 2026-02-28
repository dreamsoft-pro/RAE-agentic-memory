import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.rbac.services import EnforcerService
from apps.registry.models import Factory, Department, Line, Machine

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def manager_user(db):
    # Create user with manager role (full access to registry)
    u = User.objects.create_user(username='reg_mgr', password='password')
    
    # Initialize policies for test env
    e = EnforcerService.get_enforcer()
    e.clear_policy()
    EnforcerService.add_policy("role:manager", "registry.factory", "read")
    EnforcerService.add_policy("role:manager", "registry.factory", "write")
    EnforcerService.add_policy("role:manager", "registry.department", "write")
    EnforcerService.add_policy("role:manager", "registry.line", "write")
    EnforcerService.add_role_for_user(u.username, "role:manager")
    
    return u

@pytest.fixture
def sample_factory(db):
    return Factory.objects.create(name="Test Factory", code="TFACT-01")

@pytest.mark.django_db
class TestRegistryAPI:
    def test_factory_list(self, api_client, sample_factory, manager_user):
        api_client.force_authenticate(user=manager_user)
        url = reverse('factory-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['code'] == "TFACT-01"

    def test_factory_create(self, api_client, manager_user):
        api_client.force_authenticate(user=manager_user)
        url = reverse('factory-list')
        data = {"name": "New Factory", "code": "NFACT-99"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Factory.objects.count() == 1
        assert Factory.objects.get().code == "NFACT-99"

    def test_hierarchical_creation(self, api_client, sample_factory, manager_user):
        api_client.force_authenticate(user=manager_user)
        
        # Create Department
        dept_url = reverse('department-list')
        dept_data = {
            "factory": str(sample_factory.id),
            "name": "Assembly Dept",
            "code": "DEPT-A"
        }
        response = api_client.post(dept_url, dept_data)
        assert response.status_code == status.HTTP_201_CREATED
        dept_id = response.data['id']

        # Create Line
        line_url = reverse('line-list')
        line_data = {
            "department": dept_id,
            "name": "Line 1",
            "code": "L1"
        }
        response = api_client.post(line_url, line_data)
        assert response.status_code == status.HTTP_201_CREATED
        line_id = response.data['id']

        # Add machine tests
        EnforcerService.add_policy("role:manager", "registry.machine", "write")
        EnforcerService.add_policy("role:manager", "registry.machine", "read")
        EnforcerService.add_policy("role:manager", "registry.machine", "update")
        
        machine_url = reverse('machine-list')
        machine_data = {
            "line": line_id,
            "name": "CNC Machine",
            "code": "CNC-01"
        }
        response = api_client.post(machine_url, machine_data)
        assert response.status_code == status.HTTP_201_CREATED
        machine_id = response.data['id']

        # Test Machine with legacy connection
        from apps.legacy_integration.models import ConnectionProfile
        conn = ConnectionProfile.objects.create(name="EdgeDB", host="1.2.3.4", database="test")
        
        patch_data = {"legacy_connection": conn.id}
        response = api_client.patch(reverse('machine-detail', args=[machine_id]), patch_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['legacy_connection'] == conn.id

    def test_machine_list_filter(self, api_client, manager_user, sample_factory):
        api_client.force_authenticate(user=manager_user)
        EnforcerService.add_policy("role:manager", "registry.machine", "read")
        
        dept = Department.objects.create(factory=sample_factory, name="D1", code="D1")
        line = Line.objects.create(department=dept, name="L1", code="L1")
        Machine.objects.create(line=line, name="M1", code="M1")
        Machine.objects.create(line=line, name="M2", code="M2")

        url = reverse('machine-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

