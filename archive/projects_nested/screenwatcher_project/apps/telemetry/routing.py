from django.urls import re_path
from . import consumers
from apps.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/telemetry/(?P<machine_code>\w+)/$', consumers.TelemetryConsumer.as_asgi()),
    re_path(r'ws/telemetry/all/$', consumers.TelemetryConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
