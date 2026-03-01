from rest_framework import serializers
from .models import Dashboard, Widget

class WidgetSerializer(serializers.ModelSerializer):
    # Gridstack aliases
    x = serializers.IntegerField(source='pos_x', default=0)
    y = serializers.IntegerField(source='pos_y', default=0)
    w = serializers.IntegerField(source='width', default=4)
    h = serializers.IntegerField(source='height', default=4)
    
    # Type alias for easier frontend handling
    type = serializers.CharField(source='widget_type', read_only=True)

    class Meta:
        model = Widget
        fields = ['id', 'dashboard', 'title', 'type', 'widget_type', 'config', 'x', 'y', 'w', 'h']

class DashboardSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dashboard
        fields = ['id', 'name', 'is_public', 'is_default', 'widgets']

class MachineStatsSerializer(serializers.Serializer):
    class MachineInfoSerializer(serializers.Serializer):
        name = serializers.CharField()
        code = serializers.CharField()
        status = serializers.CharField()
        last_seen = serializers.DateTimeField()

    class OEEInfoSerializer(serializers.Serializer):
        oee = serializers.FloatField()
        availability = serializers.FloatField()
        performance = serializers.FloatField()
        quality = serializers.FloatField()

    machine = MachineInfoSerializer()
    oee = OEEInfoSerializer()
