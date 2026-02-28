# ScreenWatcher API Documentation Index

This directory contains the documentation for the ScreenWatcher REST API.

## High-Level Overview
- **[API Guide](API_GUIDE.md)** - Start here for authentication and general patterns.

## API Documentation Modules
- [Downtime API](DOWNTIME_API.md) - Tracking and categorizing machine downtime.
- [Collector API](COLLECTOR_API.md) - Telemetry ingestion from Edge clients.
- [Registry API](REGISTRY_API.md) - Management of factory structure (Factories, Lines, Machines).
- [Rules API](RULES_API.md) - Configuration and simulation of logic rules.
- [Reports API](REPORTS_API.md) - Access to generated reports and data exports.

## General Information

### Base URL
All API endpoints are prefixed with `/api/`.

### Authentication
Most endpoints require authentication.
- **Header**: `Authorization: Token <your_token>`

### Interactive Documentation
A live Swagger UI is available at:
`http://<server-ip>/api/schema/swagger-ui/`

### Schema File
The OpenAPI 3.0 specification is available at:
`/api/schema/` (or see `schema.yml` in the root directory).
