from rest_framework import serializers
from .models import Operator, ReasonCode

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'

class ReasonCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonCode
        fields = '__all__'

class DowntimeSubmissionSerializer(serializers.Serializer):
    machine_id = serializers.IntegerField(required=True)
    reason_code_id = serializers.IntegerField(required=True)
    comment = serializers.CharField(required=False, allow_blank=True)
