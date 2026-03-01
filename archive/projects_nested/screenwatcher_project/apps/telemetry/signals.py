from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import TelemetryPoint
from apps.oee.models import DailyOEE

@receiver(post_save, sender=TelemetryPoint)
def broadcast_telemetry(sender, instance, created, **kwargs):
    if created:
        try:
            channel_layer = get_channel_layer()
            data = {
                "machine_code": instance.machine.code,
                "timestamp": instance.timestamp.isoformat(),
                "payload": instance.payload,
                "type": "telemetry"
            }

            # Broadcast to specific machine group
            async_to_sync(channel_layer.group_send)(
                f"machine_{instance.machine.code}",
                {
                    "type": "machine_telemetry",
                    "data": data
                }
            )

            # Broadcast to all machines group
            async_to_sync(channel_layer.group_send)(
                "all_machines",
                {
                    "type": "machine_telemetry",
                    "data": data
                }
            )
        except Exception as e:
            # Prevent failure in DB transaction if Redis/Channels is down
            print(f"Failed to broadcast telemetry: {e}")

@receiver(post_save, sender=DailyOEE)
def broadcast_oee(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = {
        "machine_code": instance.machine.code,
        "date": instance.date.isoformat(),
        "oee": instance.oee,
        "availability": instance.availability,
        "performance": instance.performance,
        "quality": instance.quality,
        "type": "oee_update"
    }
    
    # Broadcast to specific machine group
    try:
        async_to_sync(channel_layer.group_send)(
            f"machine_{instance.machine.code}",
            {
                "type": "machine_telemetry",
                "data": data
            }
        )
    except Exception as e:
        print(f"WebSocket OEE broadcast error (Redis?): {e}")