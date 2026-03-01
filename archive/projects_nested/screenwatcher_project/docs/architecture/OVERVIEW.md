# ScreenWatcher System Architecture

## Overview
ScreenWatcher is a modular monolith designed for real-time industrial monitoring (MES-light). It tracks machine OEE (Availability, Performance, Quality) and automates downtime detection.

## Core Modules
- **Collector (`apps.collector`)**: Ingests telemetry data via REST. Validates payloads with Pydantic.
- **Telemetry (`apps.telemetry`)**: Stores raw data and broadcasts updates via WebSockets (Django Channels).
- **Rules Engine (`apps.rules`)**: Evaluates incoming data against user-defined logic (json-logic) and triggers actions.
- **OEE (`apps.oee`)**: Calculates KPIs daily and per shift. Manages automated Downtime tracking.
- **Reports (`apps.reports`)**: Generates periodic summaries (Shift Reports) and provides data exports.
- **RBAC (`apps.rbac`)**: Granular access control using Casbin.

## Data Flow
1. **Machine/Edge** sends telemetry -> `collector`.
2. `collector` updates `OEE` and `Downtime` state.
3. `telemetry` signal broadcasts raw data and OEE updates to `WebSocket` groups.
4. `rules` engine evaluates the point and creates events if thresholds are met.

## Deployment
- **Backend**: Django 5.2 (LTS) on Python 3.13.
- **Database**: MariaDB (Production) or SQLite (Dev/Test).
- **Real-time**: Redis for Channels and Celery.
- **Edge**: Python-based agent with OCR capabilities.
