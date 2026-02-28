from typing import Dict, Any, List
import re
from django.utils import timezone
from datetime import timedelta
from apps.telemetry.models import TelemetryPoint
from apps.dashboards.models import Widget
from apps.oee.models import DailyOEE, ProductionJob

class BaseWidgetProvider:
    def get_time_range(self, default_hours: int, params: Dict[str, Any] = None):
        from django.utils.dateparse import parse_datetime
        from django.utils import timezone
        start_str = params.get('from') if params else None
        end_str = params.get('to') if params else None
        start_time, end_time = None, None
        if start_str and end_str:
            try:
                start_time = parse_datetime(start_str); end_time = parse_datetime(end_str)
                if start_time and timezone.is_naive(start_time): start_time = timezone.make_aware(start_time)
                if end_time and timezone.is_naive(end_time): end_time = timezone.make_aware(end_time)
            except: pass
        if not start_time or not end_time:
            range_val = params.get('range') if params else None
            ranges = {'30s': 0.008, '1m': 0.016, '5m': 0.083, '15m': 0.25, '1h': 1, '6h': 6, '8h': 8, '12h': 12, '24h': 24, '7d': 168, '30d': 720}
            hours = ranges.get(range_val, default_hours)
            end_time = timezone.now(); start_time = end_time - timedelta(hours=hours)
        return start_time, end_time

class OEEGaugeProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        try:
            today = timezone.now().date(); r = DailyOEE.objects.filter(machine_id=machine_id, date=today).first()
            if r: return {'oee': float(r.oee) * (1.0 if float(r.oee) > 1.0 else 100.0)}
            return {'oee': 0}
        except: return {'oee': 0}

class ProductionTrendProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        import sys
        machine_id = widget.config.get('machine_id')
        start_time, end_time = self.get_time_range(24, params)
        total_hours = (end_time - start_time).total_seconds() / 3600
        bucket_minutes = 1 if total_hours <= 2 else (60 if total_hours <= 24 else 1440)
        points = TelemetryPoint.objects.filter(machine_id=machine_id, timestamp__range=(start_time, end_time)).order_by('timestamp')
        is_truejet = False
        try:
            from apps.registry.models import Machine
            m = Machine.objects.get(id=machine_id); is_truejet = 'TJ' in m.code
        except: pass
        buckets = {}
        total_production = 0.0
        if is_truejet:
            def get_num(v):
                if v is None: return None
                if isinstance(v, (int, float)): return float(v)
                # Handle cases like "341.6m2" or "341,6"
                m = re.search(r'[-+]?\d*\.\d+|\d+', str(v).replace(',', '.'))
                return float(m.group(0)) if m else None

            # 1. Extraction with deduplication by TS
            agg = {}
            for p in points:
                ts = p.timestamp
                # Try clean_area_m2 first (from our ingestion), then fallback to raw payload
                a = p.payload.get('clean_area_m2')
                if a is None:
                    a = get_num(p.payload.get('Area'))
                if a is None:
                    # Deep fallback for old payload structures
                    a = get_num(p.payload.get('metrics', {}).get('pole_2'))
                
                if a is not None:
                    # If multiple points for same second, take the max (counters grow)
                    if ts not in agg or a > agg[ts]: agg[ts] = a
            
            sorted_ts = sorted(agg.keys())
            raw_areas = [agg[ts] for ts in sorted_ts]
            
            if raw_areas:
                # 2. Median Filter (Window 5) to remove OCR flicker (e.g. 100 -> 10 -> 100)
                clean_areas = []
                for i in range(len(raw_areas)):
                    win = raw_areas[max(0, i-2):min(len(raw_areas), i+3)]
                    clean_areas.append(sorted(win)[len(win)//2])
                
                # 3. Delta calculation with Reset Detection
                last_a = 0.0
                for i, ts in enumerate(sorted_ts):
                    a = clean_areas[i]
                    inc = 0.0
                    
                    if a > last_a:
                        # Normal growth
                        inc = a - last_a
                        # Filter out impossible jumps (e.g. > 50m2 in 10s)
                        if inc > 50.0: inc = 0.0 
                    elif a < last_a * 0.5 and a > 0:
                        # Counter reset (new job started) - we treat first value of new job as increment
                        inc = a
                    
                    if inc > 0:
                        total_production += inc
                        ts_bucket = ts.replace(second=0, microsecond=0)
                        if bucket_minutes == 60: ts_bucket = ts_bucket.replace(minute=0)
                        elif bucket_minutes == 1440: ts_bucket = ts_bucket.replace(hour=0, minute=0)
                        
                        ts_str = ts_bucket.isoformat()
                        buckets[ts_str] = buckets.get(ts_str, 0.0) + inc
                    last_a = a
                
                logger.info("production_calc_finished", machine=machine_id, total=total_production)
        else:
            for p in points:
                ts_bucket = p.timestamp.replace(second=0, microsecond=0)
                if bucket_minutes == 60: ts_bucket = ts_bucket.replace(minute=0)
                elif bucket_minutes == 1440: ts_bucket = ts_bucket.replace(hour=0, minute=0)
                ts_str = ts_bucket.isoformat()
                val = p.payload.get('metrics', {}).get('parts_delta', 0) or p.payload.get('parts_delta', 0)
                try: f_val = float(val or 0); buckets[ts_str] = buckets.get(ts_str, 0) + f_val; total_production += f_val
                except: pass
        data = [[ts, round(buckets[ts], 2)] for ts in sorted(buckets.keys())]
        return {'data': data, 'total': round(total_production, 2)}

class MachineGanttProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        # Inject config dates if params are missing (Fallback to widget config)
        if params is None:
            params = {}
        else:
            params = params.copy() # Make it mutable if it's a QueryDict
            
        if not params.get('from') and widget.config.get('customStart'):
            params['from'] = widget.config.get('customStart')
        if not params.get('to') and widget.config.get('customEnd'):
            params['to'] = widget.config.get('customEnd')
            
        machine_id = widget.config.get('machine_id'); start_time, end_time = self.get_time_range(12, params)
        points = TelemetryPoint.objects.filter(machine_id=machine_id, timestamp__range=(start_time, end_time)).order_by('timestamp')
        if points.count() > 5000: points = points.iterator()
        segments = []
        def get_strict_status(p):
            payload = p.payload; val = payload.get('Speed')
            if not val:
                tbl = payload.get('metrics', {}).get('table', [])
                if isinstance(tbl, list):
                    rows = [r[0] for r in tbl if r and isinstance(r, list)]; n = len(rows)//2
                    val = dict(zip(rows[:n], rows[n:])).get('Speed') if n > 0 else None
            speed = 0.0
            if val:
                try:
                    if isinstance(val, (int, float)): speed = float(val)
                    elif isinstance(val, str):
                        m = re.search(r'\(([-+]?\d+(?:\.\d+)?)\)', val)
                        if m: speed = float(m.group(1))
                        else:
                            m = re.search(r'[-+]?\d*\.\d+|\d+', val.replace(',', '.'))
                            speed = float(m.group(0)) if m else 0.0
                except: pass
            
            # Check for parsed speed (from improved importer)
            if payload.get('clean_speed', 0) > 0:
                speed = payload.get('clean_speed')

            if speed > 10.0: return 'JOB'
            if speed > 0.0: return 'MICRO-STOP'
            return 'STOPPED'
        if not points: return {'data': []}
        try:
            cur = None
            for p in points:
                status = get_strict_status(p); ts = p.timestamp
                if cur is None: cur = {'name': status, 'start': ts, 'end': ts}
                else:
                    gap = (ts - cur['end']).total_seconds()
                    if status == cur['name'] and gap < 300: cur['end'] = ts
                    else:
                        segments.append({'name': cur['name'], 'value': [0, cur['start'].timestamp() * 1000, cur['end'].timestamp() * 1000, (cur['end'] - cur['start']).total_seconds() * 1000]})
                        if gap > 300: segments.append({'name': 'NO-DATA', 'value': [0, cur['end'].timestamp() * 1000, ts.timestamp() * 1000, gap * 1000]})
                        cur = {'name': status, 'start': ts, 'end': ts}
            if cur: segments.append({'name': cur['name'], 'value': [0, cur['start'].timestamp() * 1000, cur['end'].timestamp() * 1000, (cur['end'] - cur['start']).total_seconds() * 1000]})
        except Exception as e: sys.stderr.write(f'Gantt Error: {e}\n')
        return {'data': segments}

class OEEHeatmapProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        data = [[x, y, 50 + (x+y)%50] for x in range(24) for y in range(7)]
        return {'data': data}

class ReliabilityCardProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        try:
            today = timezone.now().date(); r = DailyOEE.objects.filter(machine_id=machine_id, date=today).first()
            if r: return {'availability': float(r.availability) * (1.0 if float(r.availability) > 1.0 else 100.0), 'performance': float(r.performance) * (1.0 if float(r.performance) > 1.0 else 100.0), 'quality': float(r.quality) * (1.0 if float(r.quality) > 1.0 else 100.0)}
        except: pass
        return {'availability': 0, 'performance': 0, 'quality': 0}

class ProductionHistoryProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        start_time, end_time = self.get_time_range(24, params)
        
        # Check if we have ANY data in this range
        exists = ProductionJob.objects.filter(machine_id=machine_id, timestamp__range=(start_time, end_time)).exists()
        
        if not exists and not params.get('from'):
            # AUTO-SHIFT: If no data in "now" range, find the latest data available
            latest = ProductionJob.objects.filter(machine_id=machine_id).order_by('-timestamp').first()
            if latest:
                end_time = latest.timestamp + timedelta(hours=1)
                start_time = end_time - timedelta(hours=24)

        jobs = ProductionJob.objects.filter(
            machine_id=machine_id, 
            timestamp__range=(start_time, end_time)
        ).order_by('timestamp')
        
        # Base response with actual range used
        base_res = {
            'range_start': start_time.timestamp() * 1000,
            'range_end': end_time.timestamp() * 1000
        }

        if widget.widget_type == 'production_efficiency':
            data = []
            for j in jobs:
                if j.time_consuming_h > 0:
                    eff = j.print_area / j.time_consuming_h
                    data.append([j.timestamp.timestamp() * 1000, round(eff, 2)])
            return {**base_res, 'data': data}
            
        elif widget.widget_type == 'ink_efficiency':
            data = []
            for j in jobs:
                if j.print_area > 0:
                    eff = j.ink_consumption_ml / j.print_area
                    data.append([j.timestamp.timestamp() * 1000, round(eff, 2)])
            return {**base_res, 'data': data}

        elif widget.widget_type == 'production_gaps':
            segments = []
            last_end_ts = None
            threshold = float(widget.config.get('microstop_threshold', 10))
            long_stop_threshold = float(widget.config.get('long_stop_threshold', 600))
            
            for j in jobs:
                start_ts = j.timestamp.timestamp() * 1000
                duration_ms = j.time_consuming_h * 3600 * 1000
                end_ts = start_ts + duration_ms
                
                if last_end_ts:
                    gap_ms = start_ts - last_end_ts
                    gap_sec = gap_ms / 1000
                    if gap_sec >= threshold:
                        status = 'MICRO-STOP' if gap_sec < long_stop_threshold else 'LONG-STOP'
                        color = '#fd7e14' if status == 'MICRO-STOP' else '#ee6666'
                        segments.append({
                            'name': f'{status} ({int(gap_sec)}s)',
                            'value': [0, last_end_ts, start_ts, gap_ms],
                            'itemStyle': {'color': color}
                        })
                
                segments.append({
                    'name': f'JOB: {j.task_name[:20]}',
                    'value': [0, start_ts, end_ts, duration_ms],
                    'itemStyle': {'color': '#91cc75'}
                })
                last_end_ts = end_ts
            return {**base_res, 'data': segments}
        
        elif widget.widget_type == 'job_list':
            return {
                **base_res,
                'data': [
                    {
                        'time': j.timestamp.isoformat(), 
                        'task': j.task_name, 
                        'area': j.print_area, 
                        'ink': j.ink_consumption_ml,
                        'status': 'CANCELLED' if j.is_cancelled else 'OK'
                    } for j in jobs
                ]
            }
        elif widget.widget_type == 'production_summary_total':
            total = sum(j.print_area for j in jobs if not j.is_cancelled)
            total_ink = sum(j.ink_consumption_ml for j in jobs)
            return {
                **base_res,
                'total_area': round(total, 2),
                'total_ink': round(total_ink, 1),
                'job_count': jobs.count()
            }
        return {'error': 'unknown history type'}

class MultiSeriesChartProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        # Inject config dates if params are missing (Fallback to widget config)
        if params is None:
            params = {}
        else:
            params = params.copy()
        
        # Support 'customStart' and 'customEnd' from widget config (Project Convention)
        if not params.get('from') and widget.config.get('customStart'):
            params['from'] = widget.config.get('customStart')
        if not params.get('to') and widget.config.get('customEnd'):
            params['to'] = widget.config.get('customEnd')
            
        # Also support my previous 'date_from' just in case
        if not params.get('from') and widget.config.get('date_from'):
             params['from'] = widget.config.get('date_from')
        if not params.get('to') and widget.config.get('date_to'):
             params['to'] = widget.config.get('date_to')

        start_time, end_time = self.get_time_range(24, params); series_data = []
        def table_to_dict(table):
            if not table or not isinstance(table, list): return {}
            rows = [r[0] for r in table if r and isinstance(r, list)]; n = len(rows)//2
            return dict(zip(rows[:n], rows[n:])) if n > 0 else {}
        series_defs = widget.series.all().select_related('machine', 'metric')
        if not series_defs.exists(): return {'series': [], 'error': 'No series configured'}
        for s in series_defs:
            points_qs = TelemetryPoint.objects.filter(machine=s.machine, timestamp__range=(start_time, end_time)).order_by('timestamp')
            total_count = points_qs.count(); step = max(1, total_count // 1000); points = points_qs.iterator(); data_points = []
            keys = s.metric.json_key.split('.'); target_key = keys[-1]
            for i, p in enumerate(points):
                if i % step != 0: continue
                val = p.payload
                try:
                    current = val
                    for k in keys:
                        if isinstance(current, dict): current = current.get(k) if k in current else current.get(k.lower())
                        elif isinstance(current, list):
                            try: idx = int(k); current = current[idx]
                            except: current = None
                        else: current = None
                    val = current
                except: val = None
                if val is None or val == '':
                    met = p.payload.get('metrics', {}); tbl = met.get('table')
                    if isinstance(met, dict) and tbl: val = table_to_dict(tbl).get(target_key)
                if val is None or val == '': continue
                try:
                    if isinstance(val, str):
                        paren_match = re.search(r'\(([-+]?\d*\.\d+|\d+)\)', val.replace(',', '.'))
                        if paren_match: val = float(paren_match.group(1))
                        else:
                            match = re.search(r'[-+]?\d*\.\d+|\d+', val.replace(',', '.')); val = float(match.group(0)) if match else None
                    else: val = float(val)
                    if val is None: continue
                    if s.metric.code == 'speed_tj' and val > 450: continue
                    if s.metric.code == 'area_tj' and val > 5000: continue
                except: continue
                data_points.append([p.timestamp.isoformat(), val])
            series_data.append({'name': s.label or f'{s.metric.name} ({s.machine.code})', 'type': s.chart_type, 'yAxisIndex': 1 if s.y_axis == 'right' else 0, 'data': data_points, 'unit': s.metric.unit, 'color': s.color or None})
        return {'series': series_data}

class WidgetDataService:
    PROVIDERS = {
        'oee_gauge': OEEGaugeProvider, 
        'production_trend': ProductionTrendProvider, 
        'oee_trend': ProductionTrendProvider, 
        'machine_gantt': MachineGanttProvider, 
        'oee_heatmap': OEEHeatmapProvider, 
        'reliability_card': ReliabilityCardProvider, 
        'multi_series_chart': MultiSeriesChartProvider,
        'production_efficiency': ProductionHistoryProvider,
        'ink_efficiency': ProductionHistoryProvider,
        'job_list': ProductionHistoryProvider,
        'production_gaps': ProductionHistoryProvider,
        'production_summary_total': ProductionHistoryProvider
    }
    @classmethod
    def get_widget_data(cls, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        p_class = cls.PROVIDERS.get(widget.widget_type)
        if not p_class: return {'error': 'unknown type'}
        return p_class().get_data(widget, params)
