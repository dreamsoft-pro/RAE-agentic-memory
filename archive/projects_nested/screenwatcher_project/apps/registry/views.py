from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.rbac.permissions import CasbinPermission
from apps.rbac.filters import CasbinFilterBackend
from .models import Factory, Department, Line, Machine, Interface
from .serializers import (
    FactorySerializer, 
    DepartmentSerializer, 
    LineSerializer, 
    MachineSerializer, 
    InterfaceSerializer
)

class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CasbinPermission]
    filter_backends = [CasbinFilterBackend]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CasbinPermission]
    filter_backends = [CasbinFilterBackend]

class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CasbinPermission]
    filter_backends = [CasbinFilterBackend]

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CasbinPermission]
    filter_backends = [CasbinFilterBackend]

class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CasbinPermission]
    filter_backends = [CasbinFilterBackend]

