from .views import TelemetrySeriesAPI, StatusHistoryAPI, WidgetDataAPI
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DashboardView, MachineStatsAPI, DashboardViewSet, WidgetViewSet, AggregateMetricsAPI, ReliabilityMetricsAPI, TelemetryTrendAPI

router = DefaultRouter()
router.register(r'management', DashboardViewSet, basename='dashboard-manage')
router.register(r'widgets', WidgetViewSet, basename='widget-manage')

urlpatterns = [
    path('api/series/', TelemetrySeriesAPI.as_view(), name='telemetry-series'),
    path('api/status_history/', StatusHistoryAPI.as_view(), name='status-history'),
    path('api/widgets/<uuid:pk>/data/', WidgetDataAPI.as_view(), name='widget-data'),

    path('', DashboardView.as_view(), name='dashboard-home'),
    path('<uuid:dashboard_id>/', DashboardView.as_view(), name='dashboard-detail'),
    path('stats/<uuid:pk>/', MachineStatsAPI.as_view(), name='dashboard-stats'),
    path('stats/reliability/<uuid:pk>/', ReliabilityMetricsAPI.as_view(), name='reliability-stats'),
    path('stats/trend/<uuid:pk>/', TelemetryTrendAPI.as_view(), name='production-trend'),
    path('metrics/aggregate/', AggregateMetricsAPI.as_view(), name='metrics-aggregate'),
    path('api/', include(router.urls)),
]
