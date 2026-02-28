# Dashboards and Visualization in ScreenWatcher

ScreenWatcher features a flexible dashboard system designed for industrial monitoring. It allows users to visualize real-time and historical data from multiple machines and metrics.

## 1. Dashboard Structure
- **Dashboard**: A collection of widgets owned by a user.
- **Widget**: A visual component (chart, card, or gauge) configured for specific data.
- **WidgetSeries**: (Advanced) Allows a single widget to display multiple data series from different machines or metrics.

## 2. Supported Widget Types

| Type Code | Name | Description |
| :--- | :--- | :--- |
| `oee_gauge` | OEE Gauge | Displays real-time OEE percentage for a single machine. |
| `production_trend` | Production Trend | Line/Bar chart showing production volume over time. |
| `oee_trend` | OEE Trend | Historical OEE performance over days/weeks. |
| `machine_gantt` | Status Gantt | Timeline chart showing machine states (Running, Idle, Error). |
| `oee_heatmap` | OEE Heatmap | 2D visualization of OEE across multiple lines and time periods. |
| `multi_series_chart` | Multi-Series Chart | **Advanced**: Allows combining multiple metrics (e.g., Temp + Speed) from multiple machines on a single axis. |

## 3. Multi-Series Charts (Custom Data Sources)
The `multi_series_chart` is the most powerful visualization tool in ScreenWatcher. It supports:
- **Multiple Machines**: Compare performance across different assets.
- **Multiple Metrics**: Overlay different telemetry keys (e.g., Ink Level vs. Ambient Temp).
- **Dual Y-Axes**: Support for different units (e.g., Temperature in °C on left, Speed in m/min on right).
- **Custom Styling**: Define colors and chart types (Line, Bar, Scatter) per series.

### Configuration Example (JSON)
Widgets are configured via the `config` field and related `WidgetSeries` models.
```json
{
  "range": "1h",
  "aggregation": "avg",
  "show_legend": true
}
```

## 4. Data Providers
Each widget type is backed by a `WidgetDataProvider` in `apps.dashboards.services.widget_data.py`. These providers:
1. Parse widget configuration.
2. Fetch data from `TelemetryPoint` or `DailyOEE` models.
3. Transform data into ECharts-compatible JSON format.

## 5. API Access
Dashboards can be managed and viewed via the following API endpoints:
- `GET /api/dashboards/`: List user dashboards.
- `GET /api/dashboards/{id}/widgets/`: List widgets in a dashboard.
- `GET /api/dashboards/widgets/{id}/data/`: Fetch transformed data for a specific widget (used by the frontend).

## 6. Frontend Integration
The system is designed to work with **ECharts**. The backend provides data in a format that can be directly mapped to ECharts `series` and `dataset` options, minimizing frontend processing.
