from django.db import models
from django.db.models import Sum, Avg
from django.utils import timezone
from apps.registry.models import Shift, Machine
from apps.oee.models import ShiftOEE, DowntimeEvent
from .models import Report
import datetime

class ShiftReportGenerator:
    @staticmethod
    def generate_shift_report(date, shift_id):
        shift = Shift.objects.get(id=shift_id)
        
        # 1. Aggregate OEE
        # Get all ShiftOEE records for this shift/date
        oee_records = ShiftOEE.objects.filter(shift=shift, date=date)
        
        if not oee_records.exists():
            return None # No data, maybe don't generate?

        total_produced = oee_records.aggregate(Sum('total_parts'))['total_parts__sum'] or 0
        avg_oee = oee_records.aggregate(Avg('oee'))['oee__avg'] or 0.0
        avg_avail = oee_records.aggregate(Avg('availability'))['availability__avg'] or 0.0
        avg_perf = oee_records.aggregate(Avg('performance'))['performance__avg'] or 0.0
        avg_qual = oee_records.aggregate(Avg('quality'))['quality__avg'] or 0.0

        # 2. Top Downtimes (Global for this shift)
        shift_start = datetime.datetime.combine(date, shift.start_time)
        shift_end = datetime.datetime.combine(date, shift.end_time)
        
        if shift_end < shift_start: # Crossing midnight
             shift_end += datetime.timedelta(days=1)
             
        # Make timezone aware
        if timezone.is_aware(shift_start):
             pass
        else:
             current_tz = timezone.get_current_timezone()
             shift_start = timezone.make_aware(shift_start, current_tz)
             shift_end = timezone.make_aware(shift_end, current_tz)
        
        downtimes = DowntimeEvent.objects.filter(
            start_time__gte=shift_start,
            start_time__lt=shift_end
        ).values('reason__description').annotate(
            total_duration=Sum('duration_seconds'),
            count=models.Count('id')
        ).order_by('-total_duration')[:5]

        # 3. Machine Breakdown
        machine_stats = []
        for rec in oee_records:
            machine_stats.append({
                "machine": rec.machine.code,
                "oee": rec.oee,
                "produced": rec.total_parts
            })

        # 4. Create Report Structure
        report_data = {
            "title": f"Shift Report: {shift.name}",
            "date": str(date),
            "summary": {
                "avg_oee": round(avg_oee, 2),
                "avg_availability": round(avg_avail, 2),
                "avg_performance": round(avg_perf, 2),
                "avg_quality": round(avg_qual, 2),
                "total_produced": total_produced
            },
            "top_downtimes": list(downtimes),
            "machine_stats": machine_stats
        }

        # 5. Save Report
        report = Report.objects.create(
            report_type='SHIFT_END',
            date=date,
            shift_name=shift.name,
            data=report_data
        )
        
        return report
