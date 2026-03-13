from rest_framework import serializers
from .models import Rule, RuleHit

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'

class RuleHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleHit
        fields = '__all__'

class SimulationSerializer(serializers.Serializer):
    logic = serializers.JSONField(help_text="JsonLogic rule definition")
    data = serializers.JSONField(help_text="Data context to evaluate against")
