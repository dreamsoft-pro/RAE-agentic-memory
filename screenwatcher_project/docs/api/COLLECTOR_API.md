# Collector API Documentation

## Overview
The Collector API is the primary entry point for telemetry data from Edge clients, IoT gateways, or sensors.

## Endpoints

### 1. Ingest Telemetry
**POST** `/api/collector/ingest/`

Ingests a packet of telemetry data for a specific machine.

### Payload Structure

```json
{
  "machine_code": "CNC_01",
  "timestamp": "2023-12-28T12:00:00Z",
  "metrics": {
    "speed": 120.5,
    "status": "RUNNING",
    "errors": [["Line 1", "E01"], ["Line 2", "E05"]]
  },
  "metadata": {
    "speed": {
      "name": "Spindle Speed",
      "unit": "RPM",
      "type": "number",
      "category": "Mechanical"
    }
  },
  "legacy_config": {}
}
```

### Fields Description

- **machine_code**: (Required) Unique identifier of the source machine.
- **timestamp**: (Optional) UTC ISO8601 string.
- **metrics**: (Required) Key-value pairs of raw telemetry data.
- **metadata**: (Optional) Semantic definitions for metrics. Used for auto-discovery and dashboard labeling.
- **legacy_config**: (Optional) DB connection settings for direct integration.

**Response:**
- `201 Created`: Data accepted and processed.
- `400 Bad Request`: Validation error (e.g., missing fields).
- `404 Not Found`: Machine with the given code does not exist.

## Processing Logic
When data is received:
1. **Validation**: Payload is validated against the Pydantic schema.
2. **Persistence**: A `TelemetryPoint` record is created.
3. **Rules Engine**: Rules are evaluated against the new data.
4. **OEE Update**: Daily OEE stats are recalculated.
5. **Downtime Management**: If `status` changed, a `DowntimeEvent` may be created or closed.
6. **Live Broadcast**: Data is sent via WebSockets to subscribed dashboard clients.
