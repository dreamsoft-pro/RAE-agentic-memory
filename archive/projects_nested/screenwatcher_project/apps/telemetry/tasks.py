from celery import shared_task
from django.utils import timezone
from django.db.models import Min, Max, Avg, Sum
from apps.registry.models import Machine
from .models import TelemetryPoint, TelemetryHourlyRollup, MetricDefinition
import datetime

@shared_task
def perform_hourly_rollup_task(hour_str=None):
    """
    Aggregates TelemetryPoint data into TelemetryHourlyRollup.
    Supports both MetricDefinition-based aggregation and simple 'kind' field aggregation.
    """
    if hour_str:
        start_time = datetime.datetime.fromisoformat(hour_str)
        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)
    else:
        now = timezone.now()
        start_time = (now - datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    
    end_time = start_time + datetime.timedelta(hours=1)
    
    machines = Machine.objects.filter(is_active=True)
    metrics_defs = list(MetricDefinition.objects.all())
    
    processed_count = 0

    for machine in machines:
        points = TelemetryPoint.objects.filter(
            machine=machine,
            timestamp__range=(start_time, end_time)
        )
        
        if not points.exists():
            continue

        # 1. Aggregation by 'kind' (Backward compatibility & legacy tests)
        distinct_kinds = points.values_list('kind', flat=True).distinct()
        for k in distinct_kinds:
            kind_points = points.filter(kind=k)
            
            # Try to extract numerical values from payload
            values = []
            for p in kind_points:
                val = p.payload
                if isinstance(val, dict) and 'value' in val:
                    val = val['value']
                try:
                    values.append(float(val))
                except (ValueError, TypeError):
                    continue
            
            if values:
                TelemetryHourlyRollup.objects.update_or_create(
                    machine=machine,
                    timestamp=start_time,
                    kind=k,
                    defaults={
                        "min_value": min(values),
                        "max_value": max(values),
                        "avg_value": sum(values) / len(values),
                        "sum_value": sum(values),
                        "count_points": len(values)
                    }
                )
        
        # 2. Aggregation by MetricDefinition (New flexible system)
        if metrics_defs:
            aggregated_data = {}
            for md in metrics_defs:
                keys = md.json_key.split('.')
                values = []
                for p in points:
                    val = p.payload
                    try:
                        for key in keys:
                            if isinstance(val, dict): 
                                val = val.get(key, 0)
                            else: 
                                val = 0
                        if val is not None:
                            values.append(float(val))
                    except (ValueError, TypeError, AttributeError):
                        continue
                
                if values:
                    if md.aggregation == 'sum': agg_val = sum(values)
                    elif md.aggregation == 'max': agg_val = max(values)
                    elif md.aggregation == 'min': agg_val = min(values)
                    else: agg_val = sum(values) / len(values)
                    aggregated_data[md.code] = agg_val

            if aggregated_data:
                TelemetryHourlyRollup.objects.update_or_create(
                    machine=machine,
                    timestamp=start_time,
                    kind='general_metrics',
                    defaults={
                        "metrics_summary": aggregated_data,
                        "count_points": points.count(),
                    }
                )
        
        processed_count += 1
                
    return f"Hourly rollup completed for {start_time}: Processed {processed_count} machines."
