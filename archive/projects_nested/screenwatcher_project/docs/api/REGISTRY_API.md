# Registry API Documentation

## Overview
The Registry API manages the physical and logical structure of the factory. It follows a hierarchy:
`Factory` > `Department` > `Line` > `Machine` > `Interface`.

## Endpoints

All endpoints support standard CRUD operations via `ModelViewSet`.

### 1. Factories
**GET/POST/PUT/PATCH/DELETE** `/api/registry/factories/`
- `code`: Unique slug (e.g., `FAC-A`).

### 2. Departments
**GET/POST/PUT/PATCH/DELETE** `/api/registry/departments/`
- Belongs to a `Factory`.

### 3. Lines
**GET/POST/PUT/PATCH/DELETE** `/api/registry/lines/`
- Belongs to a `Department`.

### 4. Machines
**GET/POST/PUT/PATCH/DELETE** `/api/registry/machines/`
- Belongs to a `Line`.
- `code`: Unique ID used for telemetry ingestion (e.g., `M-001`).
- `cycle_time_ideal`: Used for OEE Performance calculation.

### 5. Interfaces
**GET/POST/PUT/PATCH/DELETE** `/api/registry/interfaces/`
- Defines how to connect to the machine (MQTT, OPC UA, etc.).

## Filtering
Most list endpoints support filtering by parent ID (e.g., `?line=1`).
