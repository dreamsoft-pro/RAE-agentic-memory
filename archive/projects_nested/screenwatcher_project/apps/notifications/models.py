from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.rules.models import RuleHit

class Notification(BaseModel):
    LEVEL_CHOICES = (
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='INFO')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    # Optional link to the rule hit that triggered this notification
    rule_hit = models.ForeignKey(
        RuleHit, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notifications'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.level}: {self.title} for {self.user.username}"

# Signals for real-time delivery
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Notification)
def broadcast_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f"user_notifications_{instance.user.id}"
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "data": {
                    "id": instance.id,
                    "level": instance.level,
                    "title": instance.title,
                    "message": instance.message,
                    "created_at": str(instance.created_at)
                }
            }
        )
