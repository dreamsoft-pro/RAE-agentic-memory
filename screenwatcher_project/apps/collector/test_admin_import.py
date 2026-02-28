import json
import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from apps.registry.models import Machine, Factory, Department, Line
from apps.telemetry.models import TelemetryPoint

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', password='password')

@pytest.fixture
def setup_machine(db):
    f = Factory.objects.create(name="F1", code="F1")
    d = Department.objects.create(name="D1", code="D1", factory=f)
    l = Line.objects.create(name="L1", code="L1", department=d)
    return Machine.objects.create(name="Test Machine", code="TM01", line=l)

@pytest.mark.django_db
class TestAdminOfflineImport:
    def test_import_view_get(self, client, admin_user):
        """Verify the import form is accessible."""
        client.force_login(admin_user)
        url = reverse('admin:telemetry_telemetrypoint_import_offline')
        response = client.get(url)
        assert response.status_code == 200
        assert "Importuj dane" in response.content.decode('utf-8')

    def test_successful_import(self, client, admin_user, setup_machine):
        """Verify that a valid JSONL file is correctly imported."""
        client.force_login(admin_user)
        
        # Prepare sample data
        data_line = {
            "machine_code": "TM01",
            "timestamp": "2026-01-01T12:00:00Z",
            "metrics": {"status": "RUNNING", "temp": 25.5}
        }
        jsonl_content = json.dumps(data_line).encode('utf-8') + b"\n"
        
        uploaded_file = SimpleUploadedFile(
            "offline_data.jsonl", 
            jsonl_content, 
            content_type="application/octet-stream"
        )
        
        url = reverse('admin:telemetry_telemetrypoint_import_offline')
        response = client.post(url, {'jsonl_file': uploaded_file, 'process_oee': True})
        
        assert response.status_code == 302 # Redirect after success
        assert TelemetryPoint.objects.count() == 1
        
        tp = TelemetryPoint.objects.first()
        assert tp.machine.code == "TM01"
        assert tp.payload["status"] == "RUNNING"

    def test_import_with_invalid_machine(self, client, admin_user):
        """Verify that missing machine in file doesn't crash the import."""
        client.force_login(admin_user)
        
        data_line = {"machine_code": "NON_EXISTENT", "metrics": {}}
        jsonl_content = json.dumps(data_line).encode('utf-8') + b"\n"
        uploaded_file = SimpleUploadedFile("bad.jsonl", jsonl_content)
        
        url = reverse('admin:telemetry_telemetrypoint_import_offline')
        response = client.post(url, {'jsonl_file': uploaded_file})
        
        assert response.status_code == 302
        assert TelemetryPoint.objects.count() == 0 # Nothing imported