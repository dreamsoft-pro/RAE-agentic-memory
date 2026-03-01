from rest_framework import serializers
from .models import DowntimeEvent
from apps.operator_panel.models import ReasonCode

class DowntimeEventSerializer(serializers.ModelSerializer):
    reason_code = serializers.SlugRelatedField(
        source='reason',
        slug_field='code',
        queryset=ReasonCode.objects.all(),
        required=False,
        allow_null=True
    )
    reason_desc = serializers.ReadOnlyField(source='reason.description')

    class Meta:
        model = DowntimeEvent
        fields = [
            'id', 'machine', 'start_time', 'end_time', 
            'duration_seconds', 'reason', 'reason_code', 'reason_desc', 'comment'
        ]
        read_only_fields = ['id', 'machine', 'start_time', 'end_time', 'duration_seconds']
