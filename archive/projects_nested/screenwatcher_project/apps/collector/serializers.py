from rest_framework import serializers

class TelemetryIngestSerializer(serializers.Serializer):
    machine_code = serializers.CharField(help_text="Unique code of the machine")
    timestamp = serializers.DateTimeField(required=False, help_text="Data acquisition time")
    metrics = serializers.JSONField(help_text="Key-value pairs of telemetry data")
    metadata = serializers.JSONField(required=False, help_text="Metadata about metrics (names, units, types)")
    legacy_config = serializers.JSONField(required=False, help_text="Optional legacy DB connection settings")
