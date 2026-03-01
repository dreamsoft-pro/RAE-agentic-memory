from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView

from .models import Operator, ReasonCode
from .serializers import OperatorSerializer, ReasonCodeSerializer
from apps.registry.models import Machine
try:
    from apps.oee.models import DowntimeEvent
except ImportError:
    from apps.rules.models import DowntimeEvent

class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

class ReasonCodeViewSet(viewsets.ModelViewSet):
    queryset = ReasonCode.objects.all()
    serializer_class = ReasonCodeSerializer

from drf_spectacular.utils import extend_schema
from .serializers import OperatorSerializer, ReasonCodeSerializer, DowntimeSubmissionSerializer

class DowntimeSubmissionAPI(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=DowntimeSubmissionSerializer,
        responses={200: dict, 400: dict, 404: dict},
        description="Submits a reason for a machine's current or recent downtime."
    )
    def post(self, request):
        machine_id = request.data.get('machine_id')
        reason_code_id = request.data.get('reason_code_id')
        comment = request.data.get('comment', '')
        
        if not machine_id or not reason_code_id:
            return Response({"error": "Missing machine_id or reason_code_id"}, status=400)
            
        machine = get_object_or_404(Machine, pk=machine_id)
        reason = get_object_or_404(ReasonCode, pk=reason_code_id)
        
        active_event = DowntimeEvent.objects.filter(
            machine=machine,
            end_time__isnull=True
        ).last()
        
        target_event = active_event
        
        if not target_event:
            last_event = DowntimeEvent.objects.filter(
                machine=machine,
                end_time__isnull=False
            ).order_by('-end_time').last()
            
            if last_event and (timezone.now() - last_event.end_time).total_seconds() < 300:
                target_event = last_event
        
        if target_event:
            target_event.reason_code = reason.code 
            target_event.comment = comment
            target_event.save()
            return Response({"status": "updated", "event_id": target_event.id})
        else:
            return Response({"error": "No active downtime found to tag"}, status=404)

class OperatorPanelView(TemplateView):
    template_name = "operator/panel.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machines'] = Machine.objects.filter(is_active=True)
        context['reasons'] = ReasonCode.objects.filter(is_active=True).order_by('code')
        return context
