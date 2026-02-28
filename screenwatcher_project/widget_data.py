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
                return {"oee": float(r.oee) * (1.0 if float(r.oee) > 1.0 else 100.0)}
            return {"oee": 0}
        except: return {"oee": 0}

class ProductionTrendProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        import sys
        machine_id = widget.config.get('machine_id')
        start_time, end_time = self.get_time_range(24, params)
        
        # Determine bucket size based on range
        total_hours = (end_time - start_time).total_seconds() / 3600
        if total_hours <= 2: bucket_minutes = 1
        elif total_hours <= 24: bucket_minutes = 60
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
            # INTEGRATION ALGORITHM (User Provided)
            sys.stderr.write(f"DEBUG: STARTING TrueJet Logic for {machine_id}\n")
            sys.stderr.write(f"DEBUG: Range {start_time} - {end_time}\n")
            count = points.count()
            sys.stderr.write(f"DEBUG: Points found: {count}\n")
            
            # --- Helper Functions ---
            def table_to_dict(table):
                if not table or not isinstance(table, list):
                    return {}
                rows = [r[0] for r in table if r and isinstance(r, list)]
                n = len(rows) // 2
                return dict(zip(rows[:n], rows[n:])) if n > 0 else {}

            def extract_m2h(speed_raw):
                if speed_raw is None:
                    return None
                if isinstance(speed_raw, (int, float)):
                    return float(speed_raw)
                if not isinstance(speed_raw, str):
                    return None
                
                # Priority 1: User's specific format "(123.45)" inside string
                m = re.search(r"\(([-+]?\d+(?:\.\d+)?)", speed_raw)
                if m:
                    return float(m.group(1))
                
                # Priority 2: Simple number finding "123.45" anywhere
                m = re.search(r"[-+]?\d*\.\d+|\d+", speed_raw.replace(',', '.'))
                if m:
                    return float(m.group(0))
                    
                return None

            # 1. Extraction
            raw_data = []
            for i, p in enumerate(points):
                payload = p.payload
                # Strategy: Try multiple paths for Speed and Status
                
                # Path A: Flat (Found in DB)
                speed_val = extract_m2h(payload.get('Speed') or payload.get('speed'))
                status = payload.get('status')
                
                # Path B: metrics.table.Speed (User script)
                if speed_val is None or status is None:
                    metrics = payload.get('metrics', {})
                    if speed_val is None:
                        table = metrics.get('table', [])
                        tbl_dict = table_to_dict(table)
                        speed_val = extract_m2h(tbl_dict.get('Speed'))
                    
                    if status is None:
                        status = metrics.get('status')
                
                if i < 5:
                     sys.stderr.write(f"DEBUG Point {i}: Speed={speed_val}, Status={status}, PayloadKeys={list(payload.keys())}\n")

                if speed_val is not None:
                    raw_data.append({
                        'ts': p.timestamp,
                        'speed': speed_val,
                        'status': status
                    })
            
            sys.stderr.write(f"DEBUG: Raw data extracted: {len(raw_data)}\n")

            # 2. Filter (RUNNING & > 0)
            # Make status check case-insensitive and robust
            valid_data = []
            for d in raw_data:
                status_str = str(d['status']).upper() if d['status'] else ''
                if status_str == 'RUNNING' and d['speed'] > 0:
                    valid_data.append(d)
            
            sys.stderr.write(f"DEBUG: Valid data after filter: {len(valid_data)}\n")
            
            if valid_data:
                # 3. Hampel Filter (Pure Python)
                speeds = [d['speed'] for d in valid_data]
                cleaned_speeds = []
                window_size = 7
                half_window = window_size // 2
                n_sigmas = 3
                k_const = 1.4826
                n = len(speeds)
                
                for i in range(n):
                    start_idx = max(0, i - half_window)
                    end_idx = min(n, i + half_window + 1)
                    window = speeds[start_idx:end_idx]
                    
                    # Median
                    sorted_window = sorted(window)
                    median = sorted_window[len(window) // 2]
                    
                    # MAD
                    mad_vals = sorted([abs(x - median) for x in window])
                    mad = mad_vals[len(window) // 2]
                    
                    threshold = n_sigmas * k_const * mad
                    
                    if abs(speeds[i] - median) <= threshold:
                        cleaned_speeds.append(speeds[i])
                    else:
                        cleaned_speeds.append(median)

                # 4. EMA Smoothing
                smoothed_speeds = []
                alpha = 0.3
                ema = cleaned_speeds[0]
                for val in cleaned_speeds:
                    ema = alpha * val + (1 - alpha) * ema
                    smoothed_speeds.append(ema)

                # 5. Integration
                # We need to integrate over time.
                # Area = Speed (m2/h) * dt (h)
                
                MAX_GAP_SECONDS = 60.0 # If gap > 60s, assume 0 production (machine off/disconnected)

                for i in range(n - 1):
                    t1 = valid_data[i]['ts']
                    t2 = valid_data[i+1]['ts']
                    
                    dt_seconds = (t2 - t1).total_seconds()
                    
                    # SAFETY CHECK: Don't integrate over gaps/downtime
                    if dt_seconds > MAX_GAP_SECONDS:
                        continue 

                    dt_hours = dt_seconds / 3600.0
                    
                    # Integration step
                    m2_inc = smoothed_speeds[i] * dt_hours
                    total_production += m2_inc
                    
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

        return {"data": data, "total": round(total_production, 2)}

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
                        m = re.search(r"\(([-+]?\d+(?:\.\d+)?)", val)
                        if m: speed = float(m.group(1))
                        else:
                            m = re.search(r"[-+]?\d*\.\d+|\d+", val.replace(',', '.'))
                            if m: speed = float(m.group(0))
                except: pass
            
            if speed > 10.0: return 'RUNNING'
            if speed > 0.0: return 'MICRO-STOP'
            return 'STOPPED'

        if not points: return {"data": []}

        # Try/Except for iterator safety
        try:
            # We need at least one point
            first_p = None
            # Handle iterator
            if hasattr(points, 'iterator'):
                 # It's a queryset
                 first_p = points.first()
                 # If using iterator(), first() might consume? No, separate query.
                 # But above I reassigned points to iterator() if count > 5000.
                 # Let's just iterate.
                 pass

            # Simpler loop for Gantt construction
            # We need to coalesce segments.
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
                            "name": current_segment['name'],
                            "value": [0, current_segment['start'].isoformat(), current_segment['end'].isoformat(), (current_segment['end'] - current_segment['start']).total_seconds() * 1000]
                        })
                        
                        # Handle huge gap -> Force STOPPED/UNKNOWN
                        if gap > 300:
                             segments.append({
                                "name": "NO-DATA",
                                "value": [0, current_segment['end'].isoformat(), ts.isoformat(), gap * 1000]
                            })
                            
                        current_segment = {'name': status, 'start': ts, 'end': ts}
            
            # Close last
            if current_segment:
                segments.append({
                    "name": current_segment['name'],
                    "value": [0, current_segment['start'].isoformat(), current_segment['end'].isoformat(), (current_segment['end'] - current_segment['start']).total_seconds() * 1000]
                })

        except Exception as e:
            import sys
            sys.stderr.write(f"Gantt Error: {e}\n")

        return {"data": segments}

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
        return {"data": data}

class ReliabilityCardProvider(BaseWidgetProvider):
    def get_data(self, widget: Widget, params: Dict[str, Any] = None) -> Dict[str, Any]:
        machine_id = widget.config.get('machine_id')
        try:
            today = timezone.now().date()
            r = DailyOEE.objects.filter(machine_id=machine_id, date=today).first()
            if r:
                return {
                    "availability": float(r.availability) * (1.0 if float(r.availability) > 1.0 else 100.0),
                    "performance": float(r.performance) * (1.0 if float(r.performance) > 1.0 else 100.0),
                    "quality": float(r.quality) * (1.0 if float(r.quality) > 1.0 else 100.0)
                }
        except: pass
        return {"availability": 0, "performance": 0, "quality": 0}

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
            return {"series": [], "error": "No series configured"}

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
                # We can't slice with step in Django ORM easily on all DBs efficiently without ID logic,
                # but we can fetch and iterate with step, or use array slicing on evaluation.
                # Since we iterate anyway, let's just iterate with step.
            
            # Evaluate query (we need to iterate anyway)
            # Warning: Fetching 20k+ objects might be slow on Python side. 
            # Ideally use .values() or .values_list() for performance but we need .payload property logic.
            # For now, let's just fetch all and iterate with step.
            
            # Optimization: Use iterator to save memory, manually step
            points = points_qs.iterator()
            
            # Extract value from JSON payload (supports "metrics.energy")
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
                if val is None or val == "":
                    # Check if we have metrics.table and the key exists there
                    metrics = p.payload.get('metrics', {})
                    if isinstance(metrics, dict):
                        table = metrics.get('table')
                        if table:
                            tbl_dict = table_to_dict(table)
                            # Try finding the target key (e.g. 'Speed')
                            val = tbl_dict.get(target_key)

                if val is None or val == "":
                    continue
                
                try:
                    # Clean up string values (e.g., ":87.8m?" -> 87.8, "1305.41m?(232.22m)/h" -> 1305.41)
                    if isinstance(val, str):
                        # Special case: productivity strings like "1305.41m?(232.22m)/h"
                        # User expects ~300, so we should look for the value in parenthesis if it exists
                        paren_match = re.search(r"\(([-+]?\d*\.\d+|\d+)\)", val.replace(',', '.'))
                        if paren_match:
                            val = float(paren_match.group(1))
                        else:
                            # Extract first float-like number from string
                            match = re.search(r"[-+]?\d*\.\d+|\d+", val.replace(',', '.'))
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
                "name": s.label or f"{s.metric.name} ({s.machine.code})",
                "type": s.chart_type,
                "yAxisIndex": 1 if s.y_axis == 'right' else 0,
                "data": data_points,
                "unit": s.metric.unit,
                "color": s.color or None
            })
            
        return {"series": series_data}

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
        if not p_class: return {"error": "unknown type"}
        return p_class().get_data(widget, params)
