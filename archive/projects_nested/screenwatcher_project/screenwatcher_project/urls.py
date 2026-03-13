"""
URL configuration for the ScreenWatcher project.
"""
from __future__ import annotations

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.core.views import health_check

admin.site.site_header = "ScreenWatcher Administration"
admin.site.site_title = "ScreenWatcher Admin Portal"
admin.site.index_title = "Welcome to ScreenWatcher Administration Portal"

urlpatterns = [
    path('healthz/', health_check, name='health_check'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),

    # Core Health Check
    path('', include('apps.core.urls')),

    # API endpoints
    path('api/registry/', include('apps.registry.urls')),
    path('api/operator-panel/', include('apps.operator_panel.urls')),
    path('api/collector/', include('apps.collector.urls')),
    path('api/rules/', include('apps.rules.urls')),
    path('api/oee/', include('apps.oee.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('dashboard/', include('apps.dashboards.urls')),
    path('api/reports/', include('apps.reports.urls')),

    # Legacy (Disabled)
    # path('', include('apps.statistics.urls', namespace='statistics')),
    # path('configurator/', include('apps.configurator.urls', namespace='configurator')),
    # path('api/configurator/', include('apps.configurator.api_urls', namespace='configurator-api')),
    # path('api/ingest/', include('apps.data_ingestion.urls', namespace='data-ingestion')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
