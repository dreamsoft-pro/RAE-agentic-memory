# ScreenWatcher API Guide

Welcome to the ScreenWatcher REST API. This system provides endpoints for managing industrial assets, ingesting telemetry, and monitoring OEE (Overall Equipment Effectiveness).

## 1. Quick Start

### Base URL
All API requests should be made to:
`http://<server-ip>/api/`

### Authentication
ScreenWatcher uses **Token Authentication**.
1. Obtain your token (contact administrator or use the login endpoint).
2. Include the token in the `Authorization` header of every request:
   `Authorization: Token your_generated_token_here`

### Content Type
All requests and responses use `application/json`.

## 2. Core API Modules

### [Asset Registry](REGISTRY_API.md)
Manage the hierarchy of your factory:
- `Factories` -> `Departments` -> `Lines` -> `Machines`
- Endpoint: `/api/registry/machines/`

### [Data Ingestion (Collector)](COLLECTOR_API.md)
Used by Edge clients to send telemetry data:
- Endpoint: `POST /api/collector/ingest/`
- Supports real-time metrics and status updates.

### [Rules & Logic](RULES_API.md)
Define automated reasoning based on telemetry:
- Define rules using JSON-Logic.
- Trigger actions (alerts, events) when conditions are met.

### [OEE & Analytics](DOWNTIME_API.md)
Access calculated KPIs and performance metrics:
- Real-time OEE per machine.
- Downtime categorization and Pareto analysis.

## 3. Advanced Features

### Interactive Swagger UI
Explore and test the API directly from your browser:
`/api/schema/swagger-ui/`

### OpenAPI Specification
The full technical schema is available in the root directory as `openapi_screenwatcher.json` or via the `/api/schema/` endpoint.

### Audit Logging (ISO 27001)
All data modification requests (POST, PUT, DELETE) are automatically recorded in the Audit Log for compliance.
- Who changed what, when, and from which IP.

## 4. Common Error Codes
- `401 Unauthorized`: Missing or invalid token.
- `403 Forbidden`: Authenticated, but insufficient permissions (RBAC).
- `404 Not Found`: The requested resource does not exist.
- `422 Unprocessable Entity`: Validation error (check request body).
