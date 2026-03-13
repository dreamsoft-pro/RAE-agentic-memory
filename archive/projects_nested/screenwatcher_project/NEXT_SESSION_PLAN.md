# Next Session Plan: ScreenWatcher Visualization Fix

## 🚨 Critical Issue
Despite successful data import and backend API returning correct JSON (Status 200, correct timestamps and values), **charts are not rendering in the frontend**.

## 🎯 Primary Goal
Debug and fix the Frontend/ECharts layer to ensure data visibility.

## 📋 Action Items

1.  **Frontend Debugging (Browser Console is key)**:
    *   Check for `GridStack` layout issues (0 height containers?).
    *   Verify `ECharts` instance initialization (`echarts.getInstanceByDom`).
    *   Check if `setOption` is actually called with valid data.
    *   Investigate `xAxis.type: 'time'` vs data format (ISO String vs Timestamp).

2.  **Configuration Review**:
    *   Review `builder_v5.html` logic for `multi_series_chart` and `machine_gantt`.
    *   Verify if `yAxisIndex` in series matches `yAxis` definition in option.

3.  **Experimentation**:
    *   Try hardcoding a simple ECharts option in the browser console to isolate the issue.
    *   Try removing `connectNulls: false` or `dataZoom` temporarily.

## 🛠️ Context
*   **Backend**: Python/Django (`apps/dashboards`). Returns ISO Strings for dates.
*   **Frontend**: `builder_v5.html` + ECharts 5.4.3.
*   **Data**: Present in DB (`TelemetryPoint`, `ProductionJob`).