from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'level', 'title', 'message', 'is_read', 'rule_hit', 'created_at']
        read_only_fields = ['id', 'created_at']
