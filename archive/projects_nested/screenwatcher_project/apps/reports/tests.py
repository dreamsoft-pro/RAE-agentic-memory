import datetime
from django.test import TestCase
from django.utils import timezone
from apps.registry.models import Factory, Department, Line, Machine, Shift
from apps.oee.models import ShiftOEE
from apps.reports.models import Report
from apps.reports.services import ShiftReportGenerator

class ShiftReportTest(TestCase):
    def setUp(self):
        # Setup Topology
        self.factory = Factory.objects.create(name="Test Factory", code="FAC-1")
        self.dept = Department.objects.create(factory=self.factory, name="Dept 1", code="D1")
        self.line = Line.objects.create(department=self.dept, name="Line 1", code="L1")
        self.machine = Machine.objects.create(line=self.line, name="Machine 1", code="M1")
        
        # Setup Shift
        self.shift = Shift.objects.create(
            factory=self.factory,
            name="Morning Shift",
            start_time=datetime.time(6, 0),
            end_time=datetime.time(14, 0)
        )
        
        self.date = datetime.date(2025, 1, 1)

    def test_generate_report(self):
        # 1. Create ShiftOEE Data
        ShiftOEE.objects.create(
            machine=self.machine,
            shift=self.shift,
            date=self.date,
            availability=90.0,
            performance=95.0,
            quality=99.0,
            oee=84.6,
            total_parts=1000
        )
        
        # 2. Generate Report
        report = ShiftReportGenerator.generate_shift_report(self.date, self.shift.id)
        
        # 3. Verify
        self.assertIsNotNone(report)
        self.assertEqual(report.report_type, 'SHIFT_END')
        self.assertEqual(report.date, self.date)
        self.assertEqual(report.shift_name, "Morning Shift")
        
        data = report.data
        self.assertEqual(data['summary']['avg_oee'], 84.6)
        self.assertEqual(data['summary']['total_produced'], 1000)
        self.assertEqual(len(data['machine_stats']), 1)
