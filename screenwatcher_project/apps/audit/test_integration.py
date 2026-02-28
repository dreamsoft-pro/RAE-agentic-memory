import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.registry.models import Machine, Factory, Department, Line
from apps.audit.models import AuditLog

@pytest.mark.django_db
class TestAuditIntegration:
    def setup_method(self):
        from apps.audit.signals import connect_audit_signals
        connect_audit_signals()
        
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='admin', password='password')
        self.client.force_authenticate(user=self.user)
        
        self.factory = Factory.objects.create(name="Test Factory", code="test-factory")
        self.dept = Department.objects.create(name="Test Dept", code="test-dept", factory=self.factory)
        self.line = Line.objects.create(name="Test Line", code="test-line", department=self.dept)

    def test_machine_creation_audit(self):
        """ISO 27001: Verify that creating a machine is logged."""
        url = '/api/registry/machines/'
        data = {
            "code": "AUDIT-01",
            "name": "Audit Machine",
            "line": self.line.id,
            "is_active": True
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        
        # Check AuditLog
        log = AuditLog.objects.filter(action='CREATE', description__icontains='AUDIT-01').first()
        assert log is not None
        assert log.actor == self.user
        assert 'code' in log.changes
        assert log.changes['code']['new'] == 'AUDIT-01'

    def test_machine_update_audit(self):
        """ISO 27001: Verify that updating a machine is logged with specific changes."""
        machine = Machine.objects.create(code="OLD-CODE", name="Old Name", line=self.line)
        
        url = f'/api/registry/machines/{machine.id}/'
        data = {"name": "New Name"}
        
        response = self.client.patch(url, data, format='json')
        assert response.status_code == 200
        
        # Check AuditLog
        log = AuditLog.objects.filter(action='UPDATE', object_id=str(machine.id)).last()
        assert log is not None
        assert 'name' in log.changes
        assert log.changes['name']['old'] == 'Old Name'
        assert log.changes['name']['new'] == 'New Name'

    def test_unauthorized_access_is_not_audited_as_change(self):
        """Verify that failed attempts don't create model change logs but might create login logs."""
        self.client.logout()
        url = '/api/registry/machines/'
        data = {"code": "HACK-01", "name": "Hack", "line": self.line.id}
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == 403
        
        # Ensure no CREATE log was made for this machine
        assert not AuditLog.objects.filter(description__icontains='HACK-01').exists()