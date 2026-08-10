from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from importer.models import Meter, MeterPoint, MeterReading

FIXTURE = Path(__file__).resolve().parents[2] / "DTC5259515123502080915D0010.uff"


class ImportFilesCommandTest(TestCase):
    def test_imports_records(self):
        out = StringIO()
        call_command("import_files", str(FIXTURE), stdout=out)

        self.assertGreater(MeterPoint.objects.count(), 0)
        self.assertGreater(Meter.objects.count(), 0)
        self.assertGreater(MeterReading.objects.count(), 0)
