from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from pydantic import ValidationError
from drf_spectacular.utils import extend_schema

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint
from .schemas import TelemetryPayload
from .serializers import TelemetryIngestSerializer

class IngestTelemetryView(APIView):
    """
    Endpoint for ingesting telemetry data from machines/IoT gateways.
    """
    permission_object = 'telemetry.telemetrypoint'
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(request=TelemetryIngestSerializer, responses={201: {"status": "accepted"}})
    def post(self, request):
        # 1. Validation (Pydantic)
        try:
            payload = TelemetryPayload(**request.data)
        except ValidationError as e:
            return Response({"error": e.errors()}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Check if machine exists
        machine = get_object_or_404(Machine, code=payload.machine_code)

        # 2b. Handle Legacy DB Config update from Edge
        if payload.legacy_config:
            from apps.legacy_integration.models import ConnectionProfile
            cfg = payload.legacy_config
            # Update only if central config is NOT locked
            conn = machine.legacy_connection
            if not conn or not conn.use_central_config:
                profile_name = f"EdgeConfig_{machine.code}"
                conn, created = ConnectionProfile.objects.update_or_create(
                    name=profile_name,
                    defaults={
                        "host": cfg.get("host"),
                        "port": cfg.get("port", 3306),
                        "database": cfg.get("database"),
                        "user": cfg.get("user"),
                        "password": cfg.get("password", ""),
                    }
                )
                if created or machine.legacy_connection != conn:
                    machine.legacy_connection = conn
                    machine.save()
        
        # 3. Save data
        ts = payload.timestamp or timezone.now()
        if timezone.is_naive(ts):
            ts = timezone.make_aware(ts)

        tp = TelemetryPoint.objects.create(
            machine=machine,
            timestamp=ts,
            kind='telemetry_packet',
            payload=payload.metrics
        )
        
        # 4. Automatic Metric Discovery (Semantic Mapping)
        if payload.metadata:
            from apps.telemetry.models import MetricDefinition
            for m_key, m_info in payload.metadata.items():
                MetricDefinition.objects.update_or_create(
                    code=m_key,
                    defaults={
                        "name": m_info.get("name", m_key),
                        "unit": m_info.get("unit", ""),
                        "json_key": m_key, # Field name in metrics dict
                        "aggregation": "avg" if m_info.get("type") == "number" else "max"
                    }
                )
        
        # Trigger Rules Engine (Iteration 6)
        # In production, use Celery: evaluate_rules_task.delay(tp.id)
        from apps.rules.services import RuleEvaluator
        try:
            RuleEvaluator.process_telemetry(tp)
        except Exception as e:
            # Don't fail ingestion if rules fail
            print(f"Rule evaluation error: {e}")

        # Update OEE (Live Update)
        from apps.oee.services import OEECalculator, DowntimeManager
        try:
            OEECalculator.calculate_daily(machine, tp.timestamp.date())
        except Exception as e:
            print(f"OEE calculation error: {e}")
            
        # Manage Downtime Events
        status_val = payload.metrics.get('status')
        if status_val:
            try:
                DowntimeManager.process_status_change(machine, str(status_val), tp.timestamp)
            except Exception as e:
                print(f"Downtime manager error: {e}")
        
        # Option B: Burst (For specific known metrics that need indexing)
        # (We can add logic here later to extract 'status' or 'count' into specific high-speed tables if needed)

        return Response({"status": "accepted"}, status=status.HTTP_201_CREATED)