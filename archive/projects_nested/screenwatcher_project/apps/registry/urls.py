from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FactoryViewSet, DepartmentViewSet, LineSerializer, 
    LineViewSet, MachineViewSet, InterfaceViewSet
)

router = DefaultRouter()
router.register(r'factories', FactoryViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'lines', LineViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'interfaces', InterfaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]