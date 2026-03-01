import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.rbac.services import EnforcerService
from apps.registry.models import Machine, Line, Department, Factory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_rbac_policies(db):
    # Clear and set base policies for testing
    e = EnforcerService.get_enforcer()
    e.clear_policy()
    
    # Operator: read machines
    EnforcerService.add_policy("role:operator", "registry.machine", "read")
    
    # Manager: read/write machines
    EnforcerService.add_policy("role:manager", "registry.machine", "read")
    EnforcerService.add_policy("role:manager", "registry.machine", "write")
    EnforcerService.add_policy("role:manager", "registry.machine", "update")
    EnforcerService.add_policy("role:manager", "registry.machine", "delete")

@pytest.fixture
def user_operator(db):
    u = User.objects.create_user(username='op1', password='password')
    EnforcerService.add_role_for_user(u.username, "role:operator")
    return u

@pytest.fixture
def user_manager(db):
    u = User.objects.create_user(username='mgr1', password='password')
    EnforcerService.add_role_for_user(u.username, "role:manager")
    return u

@pytest.fixture
def user_stranger(db):
    return User.objects.create_user(username='stranger', password='password')

@pytest.fixture
def sample_machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="M1", code="M1", line=l)

@pytest.mark.django_db
class TestRBACPermissions:
    
    def test_stranger_cannot_read_machines(self, api_client, user_stranger, sample_machine, setup_rbac_policies):
        api_client.force_authenticate(user=user_stranger)
        response = api_client.get('/api/registry/machines/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_operator_can_read_machines(self, api_client, user_operator, sample_machine, setup_rbac_policies):
        api_client.force_authenticate(user=user_operator)
        response = api_client.get('/api/registry/machines/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_operator_cannot_create_machine(self, api_client, user_operator, sample_machine, setup_rbac_policies):
        api_client.force_authenticate(user=user_operator)
        data = {"name": "M_Hack", "code": "HACK", "line": sample_machine.line.id}
        response = api_client.post('/api/registry/machines/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_manager_can_create_machine(self, api_client, user_manager, sample_machine, setup_rbac_policies):
        api_client.force_authenticate(user=user_manager)
        data = {"name": "M2", "code": "M2", "line": sample_machine.line.id}
        response = api_client.post('/api/registry/machines/', data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_casbin_filter_machines(self, api_client, sample_machine):
        """Test that list endpoint returns only machines the user has access to."""
        user = User.objects.create_user(username='limited_user', password='password')
        e = EnforcerService.get_enforcer()
        e.clear_policy()
        
        # Give permission only to a specific machine ID
        # Format: machine_<id>
        policy_obj = f"machine_{sample_machine.id}"
        EnforcerService.add_policy("role:limited", policy_obj, "read")
        EnforcerService.add_role_for_user(user.username, "role:limited")
        
        # Create another machine (no access)
        other_machine = Machine.objects.create(
            line=sample_machine.line, 
            name="NoAccess", 
            code="NOACC"
        )
        
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/registry/machines/')
        
        assert response.status_code == status.HTTP_200_OK
        # Should only see sample_machine, not other_machine
        machine_ids = [m['id'] for m in response.data]
        assert str(sample_machine.id) in machine_ids
        assert str(other_machine.id) not in machine_ids