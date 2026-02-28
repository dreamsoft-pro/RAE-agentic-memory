import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from apps.audit.models import AuditLog
from apps.registry.models import Factory, Department, Line, Machine
from django.test import Client

@pytest.mark.django_db
class TestAuditLogging:
    def setup_method(self):
        self.user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')
        self.client = Client()
        # Note: In real scenarios, middleware needs to be active. 
        # Django's Client handles middleware.

    def test_factory_creation_audit(self):
        """Test that creating a Factory triggers an audit log."""
        from apps.audit.middleware import _thread_locals
        _thread_locals.user = self.user
        _thread_locals.ip = '127.0.0.1'

        factory = Factory.objects.create(name="Test Factory", code="TEST-F")
        
        audit_log = AuditLog.objects.filter(action=AuditLog.ACTION_CREATE, object_id=str(factory.pk)).first()
        assert audit_log is not None
        assert audit_log.actor == self.user
        assert audit_log.ip_address == '127.0.0.1'
        assert "Factory" in audit_log.description

    def test_machine_update_audit_diff(self):
        """Test that updating a Machine logs the specific field changes."""
        from apps.audit.middleware import _thread_locals
        _thread_locals.user = self.user
        
        factory = Factory.objects.create(name="F1", code="F1")
        dept = Department.objects.create(factory=factory, name="D1", code="D1")
        line = Line.objects.create(department=dept, name="L1", code="L1")
        machine = Machine.objects.create(line=line, name="M1", code="M1", cycle_time_ideal=10.0)
        
        # Clear logs from creation
        AuditLog.objects.all().delete()
        
        machine.name = "M1 Updated"
        machine.cycle_time_ideal = 15.0
        machine.save()
        
        audit_log = AuditLog.objects.filter(action=AuditLog.ACTION_UPDATE, object_id=str(machine.pk)).first()
        assert audit_log is not None
        assert 'name' in audit_log.changes
        assert audit_log.changes['name']['old'] == "M1"
        assert audit_log.changes['name']['new'] == "M1 Updated"
        assert 'cycle_time_ideal' in audit_log.changes
        assert float(audit_log.changes['cycle_time_ideal']['old']) == 10.0
        assert float(audit_log.changes['cycle_time_ideal']['new']) == 15.0

    def test_login_audit(self):
        """Test that user login is audited."""
        # Using Django Client to trigger signals through actual login
        self.client.login(username='admin', password='password123')
        
        audit_log = AuditLog.objects.filter(action=AuditLog.ACTION_LOGIN, actor=self.user).first()
        assert audit_log is not None
        assert audit_log.description == "User logged in"

    def test_login_failed_audit(self):
        """Test that failed login attempts are audited."""
        self.client.login(username='admin', password='wrongpassword')
        
        audit_log = AuditLog.objects.filter(action=AuditLog.ACTION_LOGIN_FAILED).first()
        assert audit_log is not None
        assert "Login failed for: admin" in audit_log.description
