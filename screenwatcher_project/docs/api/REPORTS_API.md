# Reports API Documentation

## Overview
Provides access to generated Shift Reports and data exports.

## Endpoints

### 1. Report Archive
**GET** `/api/reports/archive/`

Returns a list of generated reports.

**Query Parameters:**
- `report_type`: `SHIFT_END`, `DAILY_SUMMARY`, `ON_DEMAND`.
- `date`: `YYYY-MM-DD`.
- `date__gte` / `date__lte`: Date range filtering.

### 2. Export OEE (CSV)
**GET** `/api/reports/export/oee/`
Downloads a CSV file with Daily OEE data.

### 3. Export Events (CSV)
**GET** `/api/reports/export/events/`
Downloads a CSV file with Rule Hits history.
