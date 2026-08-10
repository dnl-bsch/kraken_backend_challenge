from datetime import datetime
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from importer.models import Meter, MeterPoint, MeterReading
from importer.services import parse_file, read_d0010


class Command(BaseCommand):
    help = "Reads files and imports them into the database"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = Path(options["file_path"]).expanduser().resolve()
        if not file_path.exists() or not file_path.is_file():
            raise CommandError(f"File not found: {file_path}")

        lines, source_file = parse_file(file_path)
        result = read_d0010(lines, source_file)
        source_file = result["source_file"]
        meter_points = result["meter_points"]

        counts = {
            "meter_points": 0,
            "meters": 0,
            "readings_created": 0,
            "readings_updated": 0,
        }

        with transaction.atomic():
            for meter_point_data in meter_points:
                meter_point, meter_point_created = MeterPoint.objects.get_or_create(mpan=meter_point_data["mpan"])
                counts["meter_points"] += int(meter_point_created)

                for meter_data in meter_point_data["meters"]:
                    meter, meter_created = Meter.objects.get_or_create(
                        meter_point=meter_point,
                        serial_number=meter_data["serial_number"],
                    )
                    counts["meters"] += int(meter_created)

                    for reading_data in meter_data["readings"]:
                        reading_datetime = datetime.strptime(reading_data["reading_datetime"], "%Y%m%d%H%M%S")
                        reading_datetime = timezone.make_aware(reading_datetime, timezone.get_current_timezone())
                        _, reading_created = MeterReading.objects.update_or_create(
                            meter=meter,
                            register_id=reading_data["register_id"],
                            reading_datetime=reading_datetime,
                            defaults={
                                "reading_value": Decimal(reading_data["reading_value"]),
                                "source_file": source_file,
                            },
                        )
                        if reading_created:
                            counts["readings_created"] += 1
                        else:
                            counts["readings_updated"] += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Imported "
                f"{counts['meter_points']} meter points, "
                f"{counts['meters']} meters, "
                f"{counts['readings_created']} readings created, "
                f"{counts['readings_updated']} readings updated"
            )
        )
