from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExportOEEView, ExportEventsView, ReportViewSet

router = DefaultRouter()
router.register(r'archive', ReportViewSet, basename='report')

urlpatterns = [
    path('export/oee/', ExportOEEView.as_view(), name='export-oee'),
    path('export/events/', ExportEventsView.as_view(), name='export-events'),
    path('', include(router.urls)),
]
