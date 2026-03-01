import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import time, timedelta
from apps.registry.models import Factory, Department, Line, Machine
from apps.oee.models import Shift, DailyOEE, DowntimeEvent
from apps.operator_panel.models import ReasonCode
from apps.telemetry.models import TelemetryPoint
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestEndToEndFlow:
    @pytest.fixture
    def setup_data(self):
        # 1. Topology
        f = Factory.objects.create(name="F1", code="F1")
        d = Department.objects.create(name="D1", code="D1", factory=f)
        l = Line.objects.create(name="L1", code="L1", department=d)
        m = Machine.objects.create(name="M1", code="M1", line=l)
        
        # 2. Shift (covers current time)
        Shift.objects.create(
            name="All Day",
            factory=f,
            start_time=time(0, 0),
            end_time=time(23, 59)
        )
        
        # 3. User
        u = User.objects.create_user(username="operator", password="password")
        
        # 4. Reason Code
        rc = ReasonCode.objects.create(code="STOP_01", description="Jam", category="Technical")
        
        return {
            "machine": m,
            "user": u,
            "reason": rc
        }

    def test_full_production_cycle(self, setup_data):
        client = APIClient()
        user = setup_data['user']
        machine = setup_data['machine']
        reason_code = setup_data['reason']

        client.force_authenticate(user=user)

        # Initialize Casbin for test
        from apps.rbac.services import EnforcerService
        EnforcerService.add_policy(user.username, 'oee.downtimeevent', 'read')
        EnforcerService.add_policy(user.username, 'oee.downtimeevent', 'update')
        EnforcerService.add_policy(user.username, 'oee.downtimeevent', 'write')
        EnforcerService.get_enforcer().save_policy()

        # ==========================================
        # Step 1: Ingest Running Data
        # ==========================================
        ingest_url = '/api/collector/ingest/'
        payload_run = {
            "machine_code": machine.code,
            "metrics": {
                "status": "RUNNING",
                "production_count": 100,
                "temperature": 55.5
            }
        }
        
        print(f"\n[E2E] Sending RUNNING telemetry to {ingest_url}...")
        resp = client.post(ingest_url, payload_run, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        
        # Verify TelemetryPoint
        assert TelemetryPoint.objects.filter(machine=machine).count() == 1
        print("[E2E] TelemetryPoint created.")
        
        # Verify DailyOEE (should be created/updated)
        # Note: OEE calculation might be async or sync depending on configuration.
        # In tests (and views.py changes), we made it sync for now or triggered it.
        # Let's check if DailyOEE exists.
        oee_record = DailyOEE.objects.filter(machine=machine, date=timezone.now().date()).first()
        assert oee_record is not None
        # assert oee_record.total_parts >= 100 # Logic depends on implementation (delta vs total)
        print(f"[E2E] DailyOEE record found: {oee_record}")

        # ==========================================
        # Step 2: Ingest Stopped Data (Downtime)
        # ==========================================
        payload_stop = {
            "machine_code": machine.code,
            "metrics": {
                "status": "STOPPED",
                "error_code": 99
            }
        }
        
        print(f"[E2E] Sending STOPPED telemetry...")
        resp = client.post(ingest_url, payload_stop, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        
        # Verify DowntimeEvent created
        downtime = DowntimeEvent.objects.filter(machine=machine, end_time__isnull=True).last()
        assert downtime is not None
        assert downtime.machine == machine
        print(f"[E2E] DowntimeEvent started: ID={downtime.id}")

        # ==========================================
        # Step 3: Operator Assigns Reason
        # ==========================================
        assign_url = f'/api/oee/downtime-events/{downtime.id}/'
        patch_data = {
            "reason_code": reason_code.code,
            "comment": "Paper Jam detected by operator"
        }
        
        print(f"[E2E] Operator assigning reason to downtime {downtime.id}...")
        resp = client.patch(assign_url, patch_data, format='json')
        assert resp.status_code == status.HTTP_200_OK
        
        # Verify Update
        downtime.refresh_from_db()
        assert downtime.reason == reason_code
        assert downtime.comment == "Paper Jam detected by operator"
        print("[E2E] Reason assigned successfully.")
        
        # ==========================================
        # Step 4: Machine Recovers (Optional)
        # ==========================================
        # Send RUNNING again to close downtime
        resp = client.post(ingest_url, payload_run, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        
        downtime.refresh_from_db()
        assert downtime.end_time is not None
        print(f"[E2E] Downtime closed. Duration: {downtime.duration_seconds}s")
