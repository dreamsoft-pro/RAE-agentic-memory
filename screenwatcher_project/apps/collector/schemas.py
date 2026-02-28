from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional
from datetime import datetime
from django.utils import timezone

class TelemetryPayload(BaseModel):
    machine_code: str = Field(..., description="Unique code of the machine")
    timestamp: Optional[datetime] = Field(default_factory=timezone.now, description="Data acquisition time")
    metrics: Dict[str, Any] = Field(..., description="Key-value pairs of telemetry data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata about metrics (names, units, types)")
    legacy_config: Optional[Dict[str, Any]] = Field(None, description="Optional legacy DB connection settings")

    @field_validator('metrics')
    @classmethod
    def validate_metrics(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if not v:
            raise ValueError("Metrics dictionary cannot be empty")
        return v
