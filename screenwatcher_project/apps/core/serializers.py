from rest_framework import serializers

class StatusTimelineSerializer(serializers.Serializer):
    status = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    reason = serializers.CharField()
    duration = serializers.IntegerField(help_text="Duration in seconds")

class MachineTimelineResponseSerializer(serializers.Serializer):
    machine = serializers.CharField()
    date = serializers.DateField()
    events = StatusTimelineSerializer(many=True)

class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class OEEGaugeResponseSerializer(serializers.Serializer):
    oee = serializers.FloatField()
