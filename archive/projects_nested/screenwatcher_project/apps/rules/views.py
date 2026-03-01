from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from drf_spectacular.utils import extend_schema
from django.views.generic import TemplateView

from apps.rbac.permissions import CasbinPermission
from .models import Rule, RuleHit
from .serializers import RuleSerializer, RuleHitSerializer, SimulationSerializer
from .services import RuleEvaluator

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CasbinPermission]

class RuleSimulationView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated] # Simulation is safe (read-only logic), but user must be auth.

    @extend_schema(request=SimulationSerializer, responses={200: SimulationSerializer})
    def post(self, request):
        serializer = SimulationSerializer(data=request.data)
        if serializer.is_valid():
            logic = serializer.validated_data['logic']
            data = serializer.validated_data['data']
            
            result = RuleEvaluator.evaluate(logic, data)
            
            return Response({
                "result": result,
                "logic": logic,
                "data": data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RuleEditorView(TemplateView):
    template_name = "rules/editor.html"