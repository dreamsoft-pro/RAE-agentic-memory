# Downtime API Documentation

## Overview
The ScreenWatcher Downtime module (`apps.oee`) provides automatic tracking of machine states (`RUNNING` vs `STOPPED`) and allows operators to categorize downtime events with specific reasons.

## Automatic Tracking
The system automatically tracks downtime based on telemetry data sent to the collector.
- **Start Condition:** Telemetry `status` is one of `STOPPED`, `ERROR`, `ALARM`, `DOWN`.
- **End Condition:** Telemetry `status` is one of `RUNNING`, `PRODUCTION`.

This logic is handled by the `DowntimeManager` service during telemetry ingestion.

## API Endpoints

### 1. List Downtime Events
**GET** `/api/oee/downtime-events/`

Returns a paginated list of downtime events.

**Query Parameters:**
- `machine`: (int) Filter by Machine ID.
- `start_date`: (date `YYYY-MM-DD`) Filter events starting on or after this date.
- `end_date`: (date `YYYY-MM-DD`) Filter events starting on or before this date.
- `uncategorized`: (bool `true`/`false`) If `true`, returns only events without a assigned reason.

**Response:**
```json
{
  "count": 10,
  "next": "...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "machine": 1,
      "start_time": "2025-01-01T10:00:00Z",
      "end_time": "2025-01-01T10:15:00Z",
      "duration_seconds": 900,
      "reason": null,
      "reason_code": null,
      "reason_desc": null,
      "comment": ""
    }
  ]
}
```

### 2. Update Downtime Reason
**PATCH** `/api/oee/downtime-events/{id}/`

Allows an operator to assign a reason code and comment to a specific downtime event.

**Request Body:**
```json
{
  "reason_code": "NO_MATERIAL",  // Code from ReasonCode registry
  "comment": "Waiting for forklift"
}
```

**Response:**
```json
{
  "id": 1,
  "reason_code": "NO_MATERIAL",
  "reason_desc": "Lack of raw material",
  "comment": "Waiting for forklift",
  ...
}
```

## Integration Flow
1. **Collector** receives telemetry -> Creates/Updates `DowntimeEvent`.
2. **Frontend** polls `/api/oee/downtime-events/?uncategorized=true` to show pending justifications to the operator.
3. **Operator** selects a reason -> Frontend calls `PATCH /api/oee/downtime-events/{id}/`.
