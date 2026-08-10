from django.db import models

class MeterPoint(models.Model):
    mpan = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.mpan


class Meter(models.Model):
    meter_point = models.ForeignKey(MeterPoint, on_delete=models.CASCADE, related_name="meters")
    serial_number = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["meter_point", "serial_number"], name="unique_meter_per_point"),
        ]

    def __str__(self):
        return f"{self.serial_number} ({self.meter_point.mpan})"


class MeterReading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name="readings")
    register_id = models.CharField(max_length=16)
    reading_datetime = models.DateTimeField()
    reading_value = models.DecimalField(max_digits=16, decimal_places=3)
    source_file = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["meter", "register_id", "reading_datetime"],
                name="unique_reading_per_meter_register_time",
            ),
        ]

    def __str__(self):
        return f"{self.meter.serial_number} {self.register_id} {self.reading_datetime:%Y-%m-%d %H:%M:%S}"
