from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DowntimeEventViewSet, MachineTimelineAPI

router = DefaultRouter()
router.register(r'downtime-events', DowntimeEventViewSet, basename='downtime-event')

urlpatterns = [
    path('timeline/<uuid:pk>/', MachineTimelineAPI.as_view(), name='machine-timeline'),
    path('', include(router.urls)),
]
