from typing import Dict, Any, List
import re
from django.utils import timezone
from datetime import timedelta
from apps.telemetry.models import TelemetryPoint
from apps.dashboards.models import Widget
from apps.oee.models import DailyOEE

class BaseWidgetProvider:
    def get_time_range(self, default_hours: int, params: Dict[str, Any] = None):
        from django.utils.dateparse import parse_datetime
        from django.utils import timezone
        
        start_str = params.get('from') if params else None
        end_str = params.get('to') if params else None
        
        start_time, end_time = None, None

        if start_str and end_str:
            try:
                start_time = parse_datetime(start_str)
                end_time = parse_datetime(end_str)
                
                if start_time and timezone.is_naive(start_time):
                    start_time = timezone.make_aware(start_time)
                if end_time and timezone.is_naive(end_time):
                    end_time = timezone.make_aware(end_time)
            except:
                pass

        if not start_time or not end_time:
            range_val = params.get('range') if params else None
            ranges = {
                '30s': 0.008, '1m': 0.016, '5m': 0.083, '15m': 0.25, 
                '1h': 1, '6h': 6, '8h': 8, '12h': 12, '24h': 24, '7d': 168, '30d': 720
            }
            hours = ranges.get(range_val, default_hours)
            end_time = timezone.now()
            start_time = end_time - timedelta(hours=hours)
            
        return start_time, end_time

    def get_start_time(self, default_hours: int, params: Dict[str, Any] = None):
        s, _ = self.get_time_range(default_hours, params)
        return s

class OEEGaugeProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        try:
            today = timezone.now().date()
            r = DailyOEE.objects.filter(machine_id=machine_id, date=today).first()
            if r:
                return {'oee': float(r.oee) * (1.0 if float(r.oee) > 1.0 else 100.0)}
            return {'oee': 0}
        except: return {'oee': 0}

class ProductionTrendProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        import sys
        machine_id = widget.config.get('machine_id')
        start_time, end_time = self.get_time_range(24, params)
        
        # Determine bucket size based on range
        total_hours = (end_time - start_time).total_seconds() / 3600
        if total_hours <= 2: bucket_minutes = 1
        elif total_hours <= 24: bucket_minutes = 60
                sys.stderr.write(f"DEBUG: Total Running Time: {running_time_sec}s ({running_time_sec/3600:.2f}h), Prod: {total_production}\n")
        else: bucket_minutes = 1440 # 1 day

        points = TelemetryPoint.objects.filter(
            machine_id=machine_id, 
            timestamp__range=(start_time, end_time)
        ).order_by('timestamp')
        
        # Check machine type
        is_truejet = False
        try:
            from apps.registry.models import Machine
            m = Machine.objects.get(id=machine_id)
            if 'TJ' in m.code: is_truejet = True
        except: pass

        buckets = {}
        total_production = 0.0

        if is_truejet:
            # INTEGRATION ALGORITHM (Optimized for TrueJet)
            sys.stderr.write(f'DEBUG: STARTING TrueJet Logic for {machine_id}\n')
            
            def table_to_dict(table):
                if not table or not isinstance(table, list): return {}
                rows = [r[0] for r in table if r and isinstance(r, list)]
                n = len(rows) // 2
                return dict(zip(rows[:n], rows[n:])) if n > 0 else {}

            def extract_m2h(speed_raw):
                if speed_raw is None: return None
                if isinstance(speed_raw, (int, float)): return float(speed_raw)
                if not isinstance(speed_raw, str): return None
                m = re.search(r'\(([-+]?\d+(?:\.\d+)?)', speed_raw)
                if m: return float(m.group(1))
                m = re.search(r'[-+]?\d*\.\d+|\d+', speed_raw.replace(',', '.'))
                if m: return float(m.group(0))
                return None

            # 1. Extraction (Maintain full timeline)
            raw_data = []
            for p in points:
                payload = p.payload
                speed_val = extract_m2h(payload.get('Speed') or payload.get('speed'))
                status = payload.get('status')
                if speed_val is None or status is None:
                    metrics = payload.get('metrics', {})
                    if speed_val is None:
                        speed_val = extract_m2h(table_to_dict(metrics.get('table', [])).get('Speed'))
                    if status is None:
                        status = metrics.get('status')
                
                # Append even if speed/status is missing (to maintain time gaps)
                raw_data.append({
                    'ts': p.timestamp,
                    'speed': speed_val,
                    'status': status
                })

            # 2. Clean, Sort & Deduplicate
            valid_data = []
            seen_ts = set()
            
            # Sort by TS first (crucial for time delta)
            raw_data.sort(key=lambda x: x['ts'])
            
            for d in raw_data:
                # Skip exact timestamp duplicates
                if d['ts'] in seen_ts:
                    continue
                seen_ts.add(d['ts'])
                
                # Normalize
                d['status'] = str(d['status']).upper() if d['status'] else 'UNKNOWN'
                d['speed'] = d['speed'] or 0.0
                valid_data.append(d)
            
            sys.stderr.write(f'DEBUG: Valid data (timeline): {len(valid_data)}\n')
            
            if valid_data:
                # 3. Hampel Filter & Smoothing (Apply only to speeds, preserving 0s)
                speeds = [d['speed'] for d in valid_data]
                
                # Simple cleaning: if speed is crazy high (>2000), cap it or set to 0
                cleaned_speeds = []
                for s in speeds:
                    if s > 2000: cleaned_speeds.append(0)
                    else: cleaned_speeds.append(s)

                # 4. EMA Smoothing (light)
                smoothed_speeds = []
                alpha = 0.3
                ema = cleaned_speeds[0]
                for val in cleaned_speeds:
                    ema = alpha * val + (1 - alpha) * ema
                    smoothed_speeds.append(ema)

                # 5. Integration
                # Area = Speed (m2/h) * dt (h)
                # Logic: Production occurs ONLY during the interval starting with RUNNING
                
                MAX_GAP = 300.0
                running_time_sec = 0.0 # Increased to 5 min

                for i in range(len(valid_data) - 1):
                    t1 = valid_data[i]['ts']
                    t2 = valid_data[i+1]['ts']
                    status = valid_data[i]['status']
                    
                    dt_seconds = (t2 - t1).total_seconds()
                    
                    # SAFETY CHECK: Don't integrate over huge gaps (e.g. power off)
                    if dt_seconds > MAX_GAP_SECONDS:
                        continue 

                    # Only integrate if machine was RUNNING
                    if status == 'RUNNING':
                        dt_hours = dt_seconds / 3600.0
                        
                        # Use smoothed speed for integration
                        speed_to_use = smoothed_speeds[i]
                        
                        # Guard against negative/tiny speeds noise
                        if speed_to_use < 0: speed_to_use = 0
                        
                        m2_inc = speed_to_use * dt_hours
                        total_production += m2_inc
                        running_time_sec += dt
                        
                        # Bucketing
                        ts_bucket = t1.replace(second=0, microsecond=0)
                        if bucket_minutes == 60:
                            ts_bucket = ts_bucket.replace(minute=0)
                        elif bucket_minutes == 1440:
                            ts_bucket = ts_bucket.replace(hour=0, minute=0)
                        
                        ts_str = ts_bucket.isoformat()
                        buckets[ts_str] = buckets.get(ts_str, 0.0) + m2_inc

        else:
            # DELTA LOGIC (Standard Machines)
            for p in points:
                ts_bucket = p.timestamp.replace(second=0, microsecond=0)
                if bucket_minutes == 60:
                    ts_bucket = ts_bucket.replace(minute=0)
                elif bucket_minutes == 1440:
                    ts_bucket = ts_bucket.replace(hour=0, minute=0)
                
                ts_str = ts_bucket.isoformat()
                val = p.payload.get('metrics', {}).get('parts_delta', 0) or p.payload.get('parts_delta', 0)
                try:
                    f_val = float(val or 0)
                    buckets[ts_str] = buckets.get(ts_str, 0) + f_val
                    total_production += f_val
                except: pass

        # Format for Frontend
        data = []
        sorted_keys = sorted(buckets.keys())
        for ts in sorted_keys:
            data.append([ts, round(buckets[ts], 2)])

        return {'data': data, 'total': round(total_production, 2)}

class MachineGanttProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        start_time, end_time = self.get_time_range(12, params)
        points = TelemetryPoint.objects.filter(
            machine_id=machine_id, 
            timestamp__range=(start_time, end_time)
        ).order_by('timestamp')
        
        # Downsample for Gantt if too many points
        if points.count() > 5000:
            points = points.iterator()
            
        segments = []
        # Logic: Pure Speed Threshold
        # > 10 m/h = RUNNING
        # 0.1 - 10 = MICRO-STOP (Idling)
        # 0 = STOPPED
        
        def get_strict_status(p):
            # Extract speed using same logic as other providers
            payload = p.payload
            val = payload.get('Speed')
            if not val:
                metrics = payload.get('metrics', {})
                table = metrics.get('table', [])
                if isinstance(table, list):
                    rows = [r[0] for r in table if r and isinstance(r, list)]
                    n = len(rows) // 2
                    tbl = dict(zip(rows[:n], rows[n:])) if n > 0 else {}
                    val = tbl.get('Speed')
            
            speed = 0.0
            if val:
                try:
                    if isinstance(val, (int, float)): speed = float(val)
                    elif isinstance(val, str):
                        m = re.search(r'\(([-+]?\d+(?:\.\d+)?)', val)
                        if m: speed = float(m.group(1))
                        else:
                            m = re.search(r'[-+]?\d*\.\d+|\d+', val.replace(',', '.'))
                            if m: speed = float(m.group(0))
                except: pass
            
            if speed > 10.0: return 'RUNNING'
            if speed > 0.0: return 'MICRO-STOP'
            return 'STOPPED'

        if not points: return {'data': []}

        # Try/Except for iterator safety
        try:
            current_segment = None
            
            for p in points:
                status = get_strict_status(p)
                ts = p.timestamp
                
                if current_segment is None:
                    current_segment = {'name': status, 'start': ts, 'end': ts}
                else:
                    # Check gap
                    gap = (ts - current_segment['end']).total_seconds()
                    
                    if status == current_segment['name'] and gap < 300: # 5 min tolerance for merging same status
                        current_segment['end'] = ts
                    else:
                        # Close segment
                        segments.append({
                            'name': current_segment['name'],
                            'value': [0, current_segment['start'].isoformat(), current_segment['end'].isoformat(), (current_segment['end'] - current_segment['start']).total_seconds() * 1000]
                        })
                        
                        # Handle huge gap -> Force STOPPED/UNKNOWN
                        if gap > 300:
                             segments.append({
                                'name': 'NO-DATA',
                                'value': [0, current_segment['end'].isoformat(), ts.isoformat(), gap * 1000]
                            })
                            
                        current_segment = {'name': status, 'start': ts, 'end': ts}
            
            # Close last
            if current_segment:
                segments.append({
                    'name': current_segment['name'],
                    'value': [0, current_segment['start'].isoformat(), current_segment['end'].isoformat(), (current_segment['end'] - current_segment['start']).total_seconds() * 1000]
                })

        except Exception as e:
            import sys
            sys.stderr.write(f'Gantt Error: {e}\n')

        return {'data': segments}

class OEEHeatmapProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        # Placeholder data logic for Heatmap
        # ECharts heatmap expects data in [[x, y, value], ...] format
        data = []
        # Mocking 24h x 7days grid with dummy values for now
        for x in range(24): # Hours 0-23
            for y in range(7): # Days 0-6
                data.append([x, y, 50 + (x+y)%50]) # Dummy value
        return {'data': data}

class ReliabilityCardProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        try:
            today = timezone.now().date()
            r = DailyOEE.objects.filter(machine_id=machine_id, date=today).first()
            if r:
                return {
                    'availability': float(r.availability) * (1.0 if float(r.availability) > 1.0 else 100.0),
                    'performance': float(r.performance) * (1.0 if float(r.performance) > 1.0 else 100.0),
                    'quality': float(r.quality) * (1.0 if float(r.quality) > 1.0 else 100.0)
                }
        except: pass
        return {'availability': 0, 'performance': 0, 'quality': 0}

class MultiSeriesChartProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        start_time, end_time = self.get_time_range(24, params)
        series_data = []
        
        # Helper for TrueJet table structure
        def table_to_dict(table):
            if not table or not isinstance(table, list):
                return {}
            rows = [r[0] for r in table if r and isinstance(r, list)]
            n = len(rows) // 2
            return dict(zip(rows[:n], rows[n:])) if n > 0 else {}
        
        # Optimize query: prefetch related machine/metric
        series_defs = widget.series.all().select_related('machine', 'metric')
        
        if not series_defs.exists():
            return {'series': [], 'error': 'No series configured'}

        for s in series_defs:
            # Fetch points with range
            # REMOVED HARD LIMIT [:5000] to support long ranges (e.g. 7 days)
            points_qs = TelemetryPoint.objects.filter(
                machine=s.machine, 
                timestamp__range=(start_time, end_time)
            ).order_by('timestamp')
            
            # Simple Decimation Strategy
            # If we have > 5000 points, we skip some to keep frontend fast.
            total_count = points_qs.count()
            target_count = 5000
            step = 1
            if total_count > target_count:
                step = total_count // target_count
            
            # Optimization: Use iterator to save memory, manually step
            points = points_qs.iterator()
            
            # Extract value from JSON payload (supports 'metrics.energy')
            data_points = []
            keys = s.metric.json_key.split('.')
            target_key = keys[-1]
            
            # Iterate with index to apply step
            for i, p in enumerate(points):
                if i % step != 0:
                    continue

                val = p.payload
                # ... rest of extraction logic ...
                try:
                    current = val
                    for k in keys:
                        if isinstance(current, dict):
                            current = current.get(k) if k in current else current.get(k.lower())
                        elif isinstance(current, list):
                            try:
                                idx = int(k)
                                current = current[idx]
                                if isinstance(current, list) and len(current) > 0:
                                    current = current[0]
                            except (ValueError, IndexError):
                                current = None
                        else:
                            current = None
                    
                    val = current
                except:
                    val = None

                # 2. Fallback: TrueJet Table structure logic (if val is None)
                if val is None or val == '':
                    # Check if we have metrics.table and the key exists there
                    metrics = p.payload.get('metrics', {})
                    if isinstance(metrics, dict):
                        table = metrics.get('table')
                        if table:
                            tbl_dict = table_to_dict(table)
                            # Try finding the target key (e.g. 'Speed')
                            val = tbl_dict.get(target_key)

                if val is None or val == '':
                    continue
                
                try:
                    # Clean up string values (e.g., ':87.8m?' -> 87.8, '1305.41m?(232.22m)/h' -> 1305.41)
                    if isinstance(val, str):
                        # Special case: productivity strings like '1305.41m?(232.22m)/h'
                        # User expects ~300, so we should look for the value in parenthesis if it exists
                        paren_match = re.search(r'\(([-+]?\d*\.\d+|\d+)\)', val.replace(',', '.'))
                        if paren_match:
                            val = float(paren_match.group(1))
                        else:
                            # Extract first float-like number from string
                            match = re.search(r'[-+]?\d*\.\d+|\d+', val.replace(',', '.'))
                            if match:
                                val = float(match.group(0))
                            else:
                                continue
                    else:
                        val = float(val)

                    # SANITY CHECK: OCR errors often produce huge numbers (e.g., file sizes as speed)
                    if s.metric.code == 'speed_tj' and val > 1000:
                        continue
                    if s.metric.code == 'area_tj' and val > 5000: # Adjust if needed
                        continue
                except (ValueError, TypeError):
                    continue
                    
                data_points.append([p.timestamp.isoformat(), val])

            series_data.append({
                'name': s.label or f'{s.metric.name} ({s.machine.code})',
                'type': s.chart_type,
                'yAxisIndex': 1 if s.y_axis == 'right' else 0,
                'data': data_points,
                'unit': s.metric.unit,
                'color': s.color or None
            })
            
        return {'series': series_data}

class WidgetDataService:
    PROVIDERS = {
        'oee_gauge': OEEGaugeProvider, 
        'production_trend': ProductionTrendProvider, 
        'oee_trend': ProductionTrendProvider,
        'machine_gantt': MachineGanttProvider,
        'oee_heatmap': OEEHeatmapProvider,
        'reliability_card': ReliabilityCardProvider,
        'multi_series_chart': MultiSeriesChartProvider
    }
    @classmethod
    def get_widget_data(cls, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        p_class = cls.PROVIDERS.get(widget.widget_type)
        if not p_class: return {'error': 'unknown type'}
        return p_class().get_data(widget, params)
