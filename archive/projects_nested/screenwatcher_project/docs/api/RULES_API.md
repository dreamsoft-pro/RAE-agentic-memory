# Rules API Documentation

## Overview
The Rules API allows users to define logic that is automatically evaluated when new telemetry data arrives.

## Endpoints

### 1. Rules
**GET/POST/PUT/PATCH/DELETE** `/api/rules/rules/`
- `logic`: JSON structure using `json-logic` format.
- `machine`: (Optional) Limit rule to a specific machine.

### 2. Rule Hits (History)
**GET** `/api/rules/hits/`
- History of all times a rule was triggered.
- Includes the `payload` that triggered the rule and the `action_log`.

### 3. Simulate Rule
**POST** `/api/rules/simulate/`
Allows testing a rule logic against a sample payload without saving it.

**Request Body:**
```json
{
  "logic": {"==": [{"var": "status"}, "ERROR"]},
  "data": {"status": "ERROR"}
}
```

**Response:**
```json
{
  "result": true
}
```
