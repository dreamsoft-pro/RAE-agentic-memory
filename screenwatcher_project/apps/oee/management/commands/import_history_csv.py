import csv
from django.core.management.base import BaseCommand
from apps.oee.models import ProductionJob
from apps.registry.models import Machine
from django.utils import timezone
from datetime import datetime, timedelta
import os

class Command(BaseCommand):
    help = 'Import Production History from CSV file with Start Time calculation'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')
        parser.add_argument('--machine_code', type=str, required=True, help='Code of the machine')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        machine_code = options['machine_code']
        machine = Machine.objects.get(code=machine_code)

        with open(csv_file_path, 'r', encoding='latin-1', newline='') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                try:
                    clean_row = {k.strip() if k else None: v for k, v in row.items()}
                    ts_str = clean_row.get('Date')
                    if not ts_str: continue
                    
                    # Date in CSV is END TIME
                    end_dt = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                    end_dt = timezone.make_aware(end_dt)
                    
                    def to_f(val):
                        if not val: return 0.0
                        try: return float(str(val).replace(',', '.'))
                        except: return 0.0

                    time_h = to_f(clean_row.get('Time consuming(h)'))
                    
                    # Calculate START TIME
                    start_dt = end_dt - timedelta(hours=time_h)

                    ProductionJob.objects.create(
                        machine=machine,
                        timestamp=start_dt, # We store START time as primary timestamp
                        task_name=clean_row.get('Task', 'Unknown'),
                        print_area=to_f(clean_row.get('Print Area')),
                        print_length=to_f(clean_row.get('Print Length')),
                        time_consuming_h=time_h,
                        ink_consumption_ml=to_f(clean_row.get('Ink consumption(mL)')),
                        is_cancelled=clean_row.get('Cancel') == 'Y',
                        finish_total_ratio=clean_row.get('Finish/Total', '')
                    )
                    count += 1
                except Exception as e:
                    self.stderr.write(f"Error: {e}")

        self.stdout.write(self.style.SUCCESS(f"Imported {count} jobs for {machine_code}"))
