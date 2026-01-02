

target_path = "/home/grzegorz-lesniowski/cloud/screenwatcher_project/templates/dashboards/builder.html"

new_content = """{% extends "base.html" %}
{% load static %}

{% block extra_head %}
<link href="{% static 'css/gridstack.min.css' %}" rel="stylesheet"/>
<style>
    .grid-stack { background: #f8f9fa; border: 1px dashed #ced4da; min-height: 80vh; }
    .grid-stack-item-content { background: white; border: 1px solid #dee2e6; border-radius: 5px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: flex; flex-direction: column; }
    .widget-header { background: #f1f3f5; padding: 5px 10px; font-size: 0.9rem; font-weight: bold; border-bottom: 1px solid #dee2e6; display: flex; justify-content: space-between; align-items: center; height: 40px; }
    .widget-body { padding: 10px; flex-grow: 1; width: 100%; position: relative; }
    .chart-container { width: 100%; height: 100%; min-height: 150px; }
    .btn-group-sm > .btn { margin-right: 2px; }
    .widget-controls { opacity: 0.5; transition: opacity 0.2s; }
    .grid-stack-item:hover .widget-controls { opacity: 1; }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-3 mt-2">
        <h4><span class="text-primary">Flex</span>Charts <small class="text-muted" style="font-size: 0.6em">v1.1</small></h4>

        <!-- Global Toolbar -->
        <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-secondary" onclick="openGlobalSettings()">⚙️ Global Time</button>
            <div class="vr mx-2"></div>
            <button class="btn btn-outline-primary" onclick="addNewWidget('production_trend', 'Speed Trend')">+ Speed</button>
            <button class="btn btn-outline-primary" onclick="addNewWidget('temp_trend', 'Temp Trend')">+ Temp</button>
            <button class="btn btn-outline-primary" onclick="addNewWidget('oee_gauge', 'OEE')">+ OEE</button>
            <button class="btn btn-outline-primary" onclick="addNewWidget('status_card', 'Status')">+ Status</button>

            <button class="btn btn-primary ms-3" onclick="saveDashboard()">Save Layout</button>
        </div>
    </div>

    <div class="grid-stack"></div>
</div>

<!-- Global Settings Modal -->
<div class="modal fade" id="globalSettingsModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header"><h5>Global Dashboard Settings</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <p class="text-muted">Set default time range for new widgets.</p>
                <div class="mb-3">
                    <label class="form-label">Default Range</label>
                    <select class="form-select" id="globalRange">
                        <option value="1h">Last 1 Hour</option>
                        <option value="8h">Last 8 Hours (Shift)</option>
                        <option value="24h">Last 24 Hours</option>
                        <option value="7d">Last 7 Days</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" onclick="applyGlobalSettings()">Apply to All</button>
            </div>
        </div>
    </div>
</div>

<!-- Widget Settings Modal -->
<div class="modal fade" id="widgetModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header"><h5>Widget Configuration</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <input type="hidden" id="editWidgetId">
                <div class="mb-3">
                    <label class="form-label">Title</label>
                    <input type="text" class="form-control" id="editTitle">
                </div>
                <div class="mb-3">
                    <label class="form-label">Time Range</label>
                    <select class="form-select" id="editRange">
                        <option value="1h">Last 1 Hour</option>
                        <option value="8h">Last 8 Hours</option>
                        <option value="24h">Last 24 Hours</option>
                        <option value="7d">Last 7 Days</option>
                        <option value="30d">Last 30 Days</option>
                        <option value="1y">Last Year</option>
                    </select>
                </div>
                <div class="mb-3">
                     <label class="form-label">Data Zoom</label>
                     <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="editZoom">
                        <label class="form-check-label">Show Slider</label>
                     </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" onclick="saveWidgetSettings()">Save & Refresh</button>
            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<script src="{% static 'js/gridstack.all.js' %}"></script>
<script src="{% static 'js/echarts.min.js' %}"></script>

<script>
    let grid;
    const charts = {};
    const DEFAULT_MACHINE_ID = '6eb33c58-7a60-4f9c-b9fb-d0b626410459'; // Your TM01 Machine

    // Internal state of widget configs (synced with DB/DOM)
    const widgetConfigs = {};
    // Store types to allow reloading
    const widgetTypes = {};

    document.addEventListener("DOMContentLoaded", function() {
        grid = GridStack.init({
            cellHeight: 70,
            float: true,
            removable: true,
            margin: 5
        });

        // Load existing widgets
        const widgetsDB = {{ widgets_json|safe|default:"[]" }};
        widgetsDB.forEach(w => {
            // Ensure config defaults
            w.config = w.config || {};
            if(!w.config.range) w.config.range = '1h';
            renderWidget(w);
        });

        // Global resize
        window.addEventListener('resize', () => {
            Object.values(charts).forEach(c => c.resize());
        });
    });

    function addNewWidget(type, title) {
        const id = 'new-' + Math.random().toString(36).substr(2, 9);
        const w = {
            id: id,
            widget_type: type,
            title: title,
            pos_x: 0, pos_y: 0, width: 4, height: 4,
            config: {
                machine_id: DEFAULT_MACHINE_ID,
                range: document.getElementById('globalRange').value || '1h',
                show_zoom: true
            }
        };
        renderWidget(w);
    }

    function renderWidget(w) {
        // Save state
        widgetConfigs[w.id] = w.config;
        widgetTypes[w.id] = w.widget_type;

        let content = `
            <div class="grid-stack-item-content" data-chart-type="${w.widget_type}">
                <div class="widget-header">
                    <span class="widget-title text-truncate" id="title-${w.id}">${w.title}</span>
                    <div class="widget-controls">
                        <button class="btn btn-xs btn-link text-dark p-0 me-2" onclick="openWidgetSettings('${w.id}')">⚙️</button>
                        <button class="btn btn-xs btn-link text-danger p-0" onclick="removeWidget('${w.id}')">×</button>
                    </div>
                </div>
                <div class="widget-body">
                    <div id="chart-${w.id}" class="chart-container"></div>
                </div>
            </div>`;

        grid.addWidget({x: w.pos_x, y: w.pos_y, w: w.width, h: w.height, content: content, id: w.id});

        setTimeout(() => initChart(w.id, w.widget_type), 200);
    }

    function removeWidget(id) {
        const el = document.querySelector(`.grid-stack-item[gs-id="${id}"]`);
        if(el) grid.removeWidget(el);
        delete charts[id];
        delete widgetConfigs[id];
        delete widgetTypes[id];
    }

    // --- CHART LOGIC ---

    function initChart(id, type) {
        const dom = document.getElementById('chart-' + id);
        if (!dom) return;

        // Dispose existing if any (useful for reload)
        if(charts[id]) charts[id].dispose();

        const myChart = echarts.init(dom);
        charts[id] = myChart;
        myChart.showLoading();

        loadChartData(id, type);
    }

    function loadChartData(id, type) {
        const myChart = charts[id];
        const config = widgetConfigs[id];
        const machineId = config.machine_id || DEFAULT_MACHINE_ID;

        // Calculate Times
        const now = new Date();
        let start = new Date();

        const rangeMap = {
            '1h': 1, '8h': 8, '24h': 24,
            '7d': 24*7, '30d': 24*30, '1y': 24*365
        };
        const hours = rangeMap[config.range] || 1;
        start.setHours(start.getHours() - hours);

        const isoStart = start.toISOString();
        const isoEnd = now.toISOString();

        // 1. Generic Trend API
        if (['production_trend', 'temp_trend', 'pressure_trend'].includes(type)) {
            let metric = 'speed';
            if(type === 'temp_trend') metric = 'temp';
            if(type === 'pressure_trend') metric = 'pressure';

            fetch(`/dashboard/api/series/?machine_id=${machineId}&metric=${metric}&from=${isoStart}&to=${isoEnd}`)
                .then(r => r.json())
                .then(res => {
                    myChart.hideLoading();
                    const data = res.data;

                    if(!data || data.length === 0) {
                        myChart.setOption({title:{text:'No data', left:'center', top:'center'}});
                        return;
                    }

                    const option = {
                        tooltip: { trigger: 'axis' },
                        grid: { left: 10, right: 10, bottom: config.show_zoom ? 40 : 10, top: 30, containLabel: true },
                        xAxis: { type: 'time', boundaryGap: false },
                        yAxis: { type: 'value' },
                        dataZoom: config.show_zoom ? [{ type: 'slider', bottom: 0, height: 20 }] : [],
                        series: [{
                            name: metric,
                            type: 'line',
                            smooth: true,
                            symbol: 'none',
                            data: data.map(d => [d.t, d.v]),
                            areaStyle: { opacity: 0.1 }
                        }]
                    };
                    myChart.setOption(option, true);
                });
        }
        // 2. Legacy Widgets
        else if (type === 'oee_gauge') {
             fetch('/dashboard/stats/' + machineId + '/')
                .then(r => r.json())
                .then(data => {
                    myChart.hideLoading();
                    let val = data.oee ? Math.round(data.oee.oee) : 0;
                    const option = {
                        series: [{
                            type: 'gauge',
                            progress: { show: true, width: 8 },
                            axisLine: { lineStyle: { width: 8 } },
                            detail: { valueAnimation: true, formatter: '{value}%', fontSize: 16, offsetCenter: [0, '70%'] },
                            data: [{ value: val }]
                        }]
                    };
                    myChart.setOption(option);
                });
        }
        else if (type === 'status_card') {
             fetch('/dashboard/stats/' + machineId + '/')
                .then(r => r.json())
                .then(data => {
                    myChart.hideLoading();
                    const status = data.machine.status;
                    const color = status === 'RUNNING' ? '#28a745' : (status === 'IDLE' ? '#ffc107' : '#dc3545');
                     const option = {
                        graphic: {
                            elements: [{
                                type: 'text', left: 'center', top: 'center',
                                style: { text: status, fontSize: 24, fontWeight: 'bold', fill: color }
                            }]
                        }
                    };
                    myChart.setOption(option);
                });
        }
    }

    // --- MODAL & SETTINGS ---

    function openGlobalSettings() {
        new bootstrap.Modal(document.getElementById('globalSettingsModal')).show();
    }

    function applyGlobalSettings() {
        const range = document.getElementById('globalRange').value;
        // Update all configs
        Object.keys(widgetConfigs).forEach(id => {
            widgetConfigs[id].range = range;
            // Reload chart
            initChart(id, widgetTypes[id]);
        });
        bootstrap.Modal.getInstance(document.getElementById('globalSettingsModal')).hide();
    }

    function openWidgetSettings(id) {
        const config = widgetConfigs[id];
        document.getElementById('editWidgetId').value = id;
        document.getElementById('editTitle').value = document.getElementById('title-'+id).innerText;
        document.getElementById('editRange').value = config.range || '1h';
        document.getElementById('editZoom').checked = config.show_zoom !== false;

        new bootstrap.Modal(document.getElementById('widgetModal')).show();
    }

    function saveWidgetSettings() {
        const id = document.getElementById('editWidgetId').value;
        const title = document.getElementById('editTitle').value;
        const range = document.getElementById('editRange').value;
        const zoom = document.getElementById('editZoom').checked;

        // Update UI
        document.getElementById('title-'+id).innerText = title;

        // Update Config
        widgetConfigs[id].range = range;
        widgetConfigs[id].show_zoom = zoom;

        // Reload Chart
        initChart(id, widgetTypes[id]);

        bootstrap.Modal.getInstance(document.getElementById('widgetModal')).hide();
    }

    function saveDashboard() {
        const items = grid.getGridItems();
        const widgets = items.map(item => {
            const id = item.getAttribute('gs-id');
            const type = widgetTypes[id];

            return {
                id: id.startsWith('new') ? null : id,
                type: type,
                title: document.getElementById('title-'+id).innerText,
                x: item.getAttribute('gs-x'),
                y: item.getAttribute('gs-y'),
                w: item.getAttribute('gs-w'),
                h: item.getAttribute('gs-h'),
                config: widgetConfigs[id]
            };
        });

        // We need to fetch/post logic from original file or assume standard Django save
        const dashboardId = "{{ dashboard.id }}";
        fetch(`/dashboard/api/management/${dashboardId}/save_layout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ widgets: widgets })
        })
        .then(r => r.json())
        .then(data => {
            alert("Dashboard saved successfully!");
        })
        .catch(err => alert("Error saving dashboard: " + err));
    }
</script>
{% endblock %}
"""

with open(target_path, "w") as f:
    f.write(new_content)

print(f"Overwritten {target_path}")
