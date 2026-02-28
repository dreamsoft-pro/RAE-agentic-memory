import json
import csv
import re
import logging
import uuid
from datetime import datetime
from django.utils import timezone
from django.db import transaction

from apps.collector.models import DataImport, MetricReading, MetricContext
from apps.telemetry.models import TelemetryPoint
from apps.oee.models import ProductionJob

logger = logging.getLogger(__name__)


class DataIngestionService:
    @staticmethod
    def process_import(data_import: DataImport):
        """Main entry point for processing an import file."""
        data_import.status = DataImport.Status.PROCESSING
        data_import.log = f"Started processing at {timezone.now()}\n"
        data_import.save()

        try:
            if data_import.import_type == DataImport.ImportType.SCREENWATCHER_JSONL:
                DataIngestionService._process_jsonl(data_import)
            elif data_import.import_type == DataImport.ImportType.MACHINE_LOG_CSV:
                DataIngestionService._process_csv(data_import)
            else:
                raise ValueError(f"Unknown import type: {data_import.import_type}")

            data_import.status = DataImport.Status.COMPLETED
            data_import.processed_at = timezone.now()
            data_import.log += "\nProcessing completed successfully."

        except Exception as e:
            data_import.status = DataImport.Status.FAILED
            data_import.log += f"\nERROR: {str(e)}"
            logger.exception(f"Import failed for {data_import.id}")

        finally:
            data_import.save()

    @staticmethod
    def _process_jsonl(data_import: DataImport):
        machine = data_import.machine
        count = 0
        errors = 0

        # Regex patterns for cleaning
        PATTERNS = {
            'time': re.compile(r'(\d{2}:\d{2}:\d{2})'),
            'area': re.compile(r'([\d\.]+)\s*m', re.IGNORECASE),
            'length': re.compile(r'([\d\.]+)\s*/\s*([\d\.]+)'),
            'count': re.compile(r'([\d\.]+)\s*/\s*([\d\.]+)'),
            'speed': re.compile(r'([\d\.]+)\s*m.*?/\(([\d\.]+)\s*m\)/h', re.IGNORECASE),
            'gray': re.compile(r'Gray Level:\s*(\d+)', re.IGNORECASE),
            'size': re.compile(r'(\d+)\s*x\s*(\d+)\s*mm', re.IGNORECASE),
            'path': re.compile(r'Path:(.*)', re.IGNORECASE),
            'pass': re.compile(r'Pass:\s*(\d+)', re.IGNORECASE),
            'color': re.compile(r'Color:\s*(\d+)', re.IGNORECASE),
            'filename': re.compile(r'(\d+)_(\d+)_(.*)\.prn', re.IGNORECASE)
        }

        with data_import.import_file.open('r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    if not line.strip():
                        continue
                    raw = json.loads(line)
                    metrics = raw.get('metrics', {})
                    if not metrics:
                        continue

                    # 1. Base Timestamp
                    ts_str = raw.get('timestamp')
                    ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00')) if ts_str else timezone.now()

                    # 2. Extract Raw Fields
                    raw_fields = {
                        'time': metrics.get('pole_1'),
                        'area': metrics.get('pole_2'),
                        'length': metrics.get('pole_3'),
                        'count': metrics.get('pole_4'),
                        'speed': metrics.get('pole_5'),
                        'surplus': metrics.get('pole_6'),
                        'gray': metrics.get('pole_7'),
                        'size': metrics.get('pole_8'),
                        'path': metrics.get('pole_9'),
                        'pass_val': metrics.get('pole_10'),
                        'color': metrics.get('pole_11'),
                        'status': metrics.get('status', 'UNKNOWN')
                    }

                    # 3. Process into Metrics (Readings and Context)
                    group_id = uuid.uuid4()
                    readings = []
                    contexts = []

                    # Helper to add numeric metric
                    def add_num(name, val):
                        if val is not None:
                            readings.append(MetricReading(
                                machine=machine, timestamp=ts, name=name,
                                value=float(val), group_id=group_id
                            ))

                    # Helper to add text context
                    def add_ctx(key, val):
                        if val is not None:
                            contexts.append(MetricContext(
                                machine=machine, timestamp=ts, key=key,
                                value=str(val), group_id=group_id
                            ))

                    # Status
                    add_ctx('status', raw_fields['status'])

                    # Time
                    if raw_fields['time']:
                        m = PATTERNS['time'].search(raw_fields['time'])
                        if m:
                            add_ctx('job_time', m.group(1))

                    # Area
                    if raw_fields['area']:
                        m = PATTERNS['area'].search(raw_fields['area'])
                        if m:
                            add_num('area_m2', m.group(1))

                    # Length
                    if raw_fields['length']:
                        m = PATTERNS['length'].search(raw_fields['length'])
                        if m:
                            add_num('length_done_m', m.group(1))
                            add_num('length_total_m', m.group(2))

                    # Count
                    if raw_fields['count']:
                        m = PATTERNS['count'].search(raw_fields['count'])
                        if m:
                            add_num('count_done', m.group(1))
                            add_num('count_total', m.group(2))

                    # Speed
                    if raw_fields['speed']:
                        val_str = raw_fields['speed'].replace(',', '.')
                        m = re.search(r'([\d\.]+)\s*m.*?\(([\d\.]+)\s*m', val_str, re.IGNORECASE)
                        speed_m2h = 0.0
                        speed_linear_mh = 0.0

                        if m:
                            speed_m2h = float(m.group(1))
                            speed_linear_mh = float(m.group(2))
                        else:
                            m_simple = re.search(r'(\d+\.\d+|\d+)', val_str)
                            if m_simple:
                                speed_m2h = float(m_simple.group(1))

                        # Safety Guard for TrueJet machines (OCR Noise Filter)
                        # Max realistic speed ~450 m2/h. Higher values are OCR errors (e.g. 1200).
                        if 'TJ' in machine.code or 'TrueJet' in machine.name:
                            if speed_m2h > 450:
                                speed_m2h = 0.0
                                # logger.warning(f"Filtered unrealistic speed {speed_m2h} for {machine.code}")

                        if speed_m2h > 0:
                            add_num('speed_m2h', speed_m2h)
                        
                        if speed_linear_mh > 0:
                            add_num('speed_linear_mh', speed_linear_mh)

                    # Gray Level & Tech params
                    if raw_fields['gray']:
                        m = PATTERNS['gray'].search(raw_fields['gray'])
                        if m:
                            add_num('gray_level', m.group(1))

                    if raw_fields['pass_val']:
                        m = PATTERNS['pass'].search(raw_fields['pass_val'])
                        if m:
                            add_num('pass_count', m.group(1))

                    if raw_fields['color']:
                        m = PATTERNS['color'].search(raw_fields['color'])
                        if m:
                            add_num('color_profile', m.group(1))

                    # Size
                    if raw_fields['size']:
                        m = PATTERNS['size'].search(raw_fields['size'])
                        if m:
                            add_num('width_mm', m.group(1))
                            add_num('height_mm', m.group(2))

                    # Path & Order Parsing
                    order_id_val = ''
                    position_id_val = ''
                    bryt_id_val = ''
                    full_path = ''  # Initialize full_path
                    filename = ''   # Initialize filename
                    if raw_fields['path']:
                        m = PATTERNS['path'].search(raw_fields['path'])
                        if m:
                            full_path = m.group(1).strip()
                            add_ctx('file_path', full_path)
                            filename = full_path.split('\\')[-1]
                            add_ctx('filename', filename)
                            fm = PATTERNS['filename'].search(filename)
                            if fm:
                                add_ctx('order_id', fm.group(1))
                                add_ctx('position_id', fm.group(2))
                                add_ctx('bryt_id', fm.group(3))

                    # 4. Atomic Save to Django DB
                    with transaction.atomic():
                        MetricReading.objects.bulk_create(readings)
                        MetricContext.objects.bulk_create(contexts)
                        # Keep raw point for backward compatibility/audit
                        TelemetryPoint.objects.update_or_create(
                            machine=machine, timestamp=ts, defaults={'payload': raw}
                        )
                    
                    count += 1

                except Exception as e:
                    errors += 1
                    if errors <= 10:
                        data_import.log += f"Line {line_num}: {str(e)}\n"

        data_import.log += f"\nProcessed {count} records. Errors: {errors}"

    @staticmethod
    def _process_csv(data_import: DataImport):
        machine = data_import.machine
        count = 0
        try:
            content = data_import.import_file.read().decode('utf-8')
        except UnicodeDecodeError:
            data_import.import_file.seek(0)
            content = data_import.import_file.read().decode('latin-1')

        decoded_file = content.splitlines()
        reader = csv.DictReader(decoded_file)

        with transaction.atomic():
            for row in reader:
                try:
                    row = {k.strip(): v.strip() for k, v in row.items() if k}
                    ts_str = row.get('Date')
                    if not ts_str:
                        continue
                    ts = timezone.make_aware(datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S"))

                    group_id = uuid.uuid4()

                    # Store as production metrics
                    MetricReading.objects.bulk_create([
                        MetricReading(
                            machine=machine, timestamp=ts, name='ink_ml', group_id=group_id,
                            value=float(row.get('Ink consumption(mL)', 0))
                        ),
                        MetricReading(
                            machine=machine, timestamp=ts, name='print_area_m2', group_id=group_id,
                            value=float(row.get('Print Area', 0))
                        ),
                        MetricReading(
                            machine=machine, timestamp=ts, name='print_length_m', group_id=group_id,
                            value=float(row.get('Print Length', 0))
                        ),
                        MetricReading(
                            machine=machine, timestamp=ts, name='time_h', group_id=group_id,
                            value=float(row.get('Time consuming(h)', 0))
                        ),
                    ])

                    MetricContext.objects.create(
                        machine=machine, timestamp=ts, key='task_name',
                        value=row.get('Task', 'Unknown'), group_id=group_id
                    )

                    # Legacy support for ProductionJob table
                    ProductionJob.objects.update_or_create(
                        machine=machine, timestamp=ts, task_name=row.get('Task', 'Unknown'),
                        defaults={
                            'print_area': float(row.get('Print Area', 0)),
                            'print_length': float(row.get('Print Length', 0)),
                            'time_consuming_h': float(row.get('Time consuming(h)', 0)),
                            'ink_consumption_ml': float(row.get('Ink consumption(mL)', 0)),
                            'is_cancelled': row.get('Cancel', 'N').upper() == 'Y',
                            'finish_total_ratio': row.get('Finish/Total', '')
                        }
                    )
                    
                    count += 1
                except Exception as e:
                    data_import.log += f"CSV Row Error: {str(e)}\n"

        data_import.log += f"\nImported {count} jobs from CSV."

