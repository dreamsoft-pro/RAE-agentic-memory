from django.urls import path
from .views import IngestTelemetryView

urlpatterns = [
    path('ingest/', IngestTelemetryView.as_view(), name='collector-ingest'),
]
