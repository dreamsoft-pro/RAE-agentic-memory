import os
import sys
import json
import csv
import re
from datetime import datetime, timedelta
from pathlib import Path
import django
from django.utils import timezone
from django.conf import settings

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint, MetricDefinition
from apps.dashboards.models import Dashboard, Widget, WidgetSeries
from apps.oee.models import ProductionJob

DATA_DIR = Path('docs/data-for-charts')
LOG_FILE = DATA_DIR / '_2026-01-20-16-11-40-offline_data.jsonl'
CSV_FILE = DATA_DIR / '_2026-01-20-16-11-40-774.csv'

SPEED_REGEX_FULL = re.compile(r"Speed:\s*(\d+\.?\d*)m\?\((\d+\.?\d*)m\)/h")
SPEED_REGEX_PARTIAL = re.compile(r"(\d+\.?\d*)m\)/h")
WIDTH_REGEX = re.compile(r"Size:\s*(\d+)x")

def get_or_create_machine():
    machine = Machine.objects.filter(name__icontains="TrueJet2").first()
    if not machine: machine = Machine.objects.filter(code="M01").first()
    if not machine:
        from apps.registry.models import Factory, Department, Line
        f, _ = Factory.objects.get_or_create(name="Default Factory")
        d, _ = Department.objects.get_or_create(name="Default Dept", factory=f)
        l, _ = Line.objects.get_or_create(name="Default Line", department=d)
        machine = Machine.objects.create(name="TrueJet2", code="M01", line=l)
    return machine

def setup_metrics():
    m_clean_speed, _ = MetricDefinition.objects.get_or_create(code='clean_speed', defaults={'name': 'Real Speed (Log)', 'unit': 'm2/h', 'json_key': 'clean_speed', 'aggregation': 'avg'})
    m_is_running, _ = MetricDefinition.objects.get_or_create(code='is_running', defaults={'name': 'Machine Status', 'unit': 'bool', 'json_key': 'is_running', 'aggregation': 'max'})
    m_job_area, _ = MetricDefinition.objects.get_or_create(code='job_area', defaults={'name': 'Job Area (CSV)', 'unit': 'm2', 'json_key': 'area_m2', 'aggregation': 'sum'})
    return m_clean_speed, m_is_running, m_job_area

def import_logs(machine):
    print(f"Importing Logs...")
    if not LOG_FILE.exists(): return
    
    # CLEAR OLD LOGS to allow re-import with better parsing
    # Delete logs from 19th onwards
    TelemetryPoint.objects.filter(machine=machine, kind='machine_log', timestamp__gte='2026-01-19 00:00:00').delete()
    print("Deleted old logs to re-import.")

    points_created = 0
    last_width_m = 1.5 # Default width if missing
    
    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                ts_str = data.get('timestamp')
                ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                
                metrics = data.get('metrics', {})
                pole_text = metrics.get('pole_1', '')
                status = metrics.get('status', 'UNKNOWN')
                
                speed_m2h = 0.0
                speed_mh = 0.0
                
                # 1. Parse Width (to update state)
                w_match = WIDTH_REGEX.search(pole_text)
                if w_match:
                    last_width_m = float(w_match.group(1)) / 1000.0
                
                # 2. Parse Speed
                full_match = SPEED_REGEX_FULL.search(pole_text)
                if full_match:
                    speed_m2h = float(full_match.group(1))
                    speed_mh = float(full_match.group(2))
                else:
                    # Fallback
                    part_match = SPEED_REGEX_PARTIAL.search(pole_text)
                    if part_match:
                        speed_mh = float(part_match.group(1))
                        speed_m2h = speed_mh * last_width_m

                # Sanity
                clean_speed = 0 if speed_m2h > 450 else speed_m2h
                
                # Status logic: If speed > 0, it is running, even if status says STOPPED? 
                # Trust speed.
                is_running = 1 if (status == "RUNNING" or clean_speed > 5) else 0

                payload = {
                    "source": "log_import",
                    "raw_status": status,
                    "ocr_text": pole_text,
                    "speed_m2h": speed_m2h,
                    "speed_mh": speed_mh,
                    "clean_speed": clean_speed,
                    "is_running": is_running,
                    "width_m": last_width_m
                }
                
                TelemetryPoint.objects.create(
                    machine=machine,
                    timestamp=ts,
                    kind='machine_log',
                    payload=payload
                )
                points_created += 1
            except Exception as e:
                # print(f"Err: {e}")
                pass
                
    print(f"Imported {points_created} log points.")

def import_csv(machine):
    print(f"Importing CSV Jobs...")
    if not CSV_FILE.exists(): return

    # ProductionJob.objects.filter(machine=machine, timestamp__gte='2026-01-19').delete() 
    # Optional: clear old jobs? DictReader logic handles duplication poorly without ID check.
    # get_or_create handles it.

    jobs_created = 0
    encodings = ['cp1250', 'latin-1', 'utf-8']
    
    for enc in encodings:
        try:
            with open(CSV_FILE, 'r', encoding=enc) as f:
                header_line = f.readline()
                fieldnames = [h.strip() for h in header_line.split(',') if h.strip()]
                reader = csv.DictReader(f, fieldnames=fieldnames)
                
                for row in reader:
                    try:
                        date_str = row.get('Date')
                        if not date_str: continue
                        ts = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        if settings.USE_TZ: ts = timezone.make_aware(ts)
                        
                        area = float(row.get('Print Area', 0))
                        duration_h = float(row.get('Time consuming(h)', 0))
                        ink = float(row.get('Ink consumption(mL)', 0))
                        task = row.get('Task', 'Unknown')
                        
                        # 1. Create TelemetryPoint (for Combo Chart)
                        avg_speed = area / duration_h if duration_h > 0 else 0
                        tp_payload = {
                            "source": "csv_job",
                            "job_id": row.get('ID'),
                            "task_name": task,
                            "area_m2": area,
                            "duration_h": duration_h,
                            "avg_speed_m2h": avg_speed,
                            "ink_ml": ink
                        }
                        TelemetryPoint.objects.get_or_create(
                            machine=machine,
                            timestamp=ts,
                            kind='job_finished',
                            defaults={'payload': tp_payload}
                        )
                        
                        # 2. Create ProductionJob (for KPI Widgets)
                        ProductionJob.objects.get_or_create(
                            machine=machine,
                            timestamp=ts,
                            task_name=task,
                            defaults={
                                'print_area': area,
                                'time_consuming_h': duration_h,
                                'ink_consumption_ml': ink,
                                'is_cancelled': row.get('Cancel', 'N') == 'Y'
                            }
                        )

                        jobs_created += 1
                    except Exception: continue
            print(f"Successfully imported jobs with {enc}. Count: {jobs_created}")
            break
        except UnicodeDecodeError: continue
        except Exception as e: print(f"Error: {e}"); break

def create_dashboard(machine):
    print("Updating Dashboard Configuration...")
    dash, _ = Dashboard.objects.get_or_create(
        name="Analiza Produkcji 20 Stycznia",
        defaults={"is_public": True, "user_id": 1}
    )
    
    # Refresh Widgets
    Widget.objects.filter(dashboard=dash).delete()
    m_clean_speed, m_is_running, m_job_area = setup_metrics()
    
    DASH_CONFIG = {
        "range": "custom",
        "customStart": "2026-01-19T14:00:00",
        "customEnd": "2026-01-20T18:00:00",
        "machine_id": str(machine.id),
        "connectNulls": False
    }

    # Widget 1: Multi-Series Chart (with Explicit Axes)
    # Config copied structure from reference dashboard
    CHART_CONFIG = {
        **DASH_CONFIG,
        "xAxis": {
            "type": "time",
            "title": "Time"
        },
        "yAxis": [
            {
                "type": "value",
                "name": "Prędkość (m2/h)",
                "position": "left",
                "min": 0,
                "max": 450
            },
            {
                "type": "value",
                "name": "Powierzchnia (m2)",
                "position": "right"
            }
        ]
    }

    w_chart = Widget.objects.create(
        dashboard=dash,
        title="Wydajność Maszyny (Logi) i Produkcja (CSV)",
        widget_type="multi_series_chart",
        pos_x=0, pos_y=0, width=12, height=6,
        config=CHART_CONFIG
    )
    
    WidgetSeries.objects.create(widget=w_chart, metric=m_clean_speed, machine=machine, label="Prędkość (m2/h)", y_axis="left", chart_type="line", color="#3398DB", order=1)
    WidgetSeries.objects.create(widget=w_chart, metric=m_job_area, machine=machine, label="Zadanie (m2)", y_axis="right", chart_type="bar", color="#9B59B6", order=2)

    # Widget 2: Gantt Chart
    Widget.objects.create(
        dashboard=dash,
        title="Oś Czasu (Gantt)",
        widget_type="machine_gantt",
        pos_x=0, pos_y=6, width=12, height=4,
        config={**DASH_CONFIG, "microstop_threshold": 30}
    )

    # Widget 3: Job List
    Widget.objects.create(
        dashboard=dash,
        title="Lista Zadań (CSV)",
        widget_type="job_list",
        pos_x=0, pos_y=10, width=8, height=6,
        config=DASH_CONFIG
    )
    
    # KPIs
    Widget.objects.create(
        dashboard=dash,
        title="Wydajność Średnia",
        widget_type="production_efficiency",
        pos_x=8, pos_y=10, width=4, height=3,
        config=DASH_CONFIG
    )
    Widget.objects.create(
        dashboard=dash,
        title="Suma Produkcji",
        widget_type="production_summary_total",
        pos_x=8, pos_y=13, width=4, height=3,
        config=DASH_CONFIG
    )

    print(f"Dashboard: http://localhost:9000/dashboard/{dash.id}/")

def run():
    machine = get_or_create_machine()
    import_logs(machine)
    import_csv(machine)
    create_dashboard(machine)

if __name__ == "__main__":
    run()