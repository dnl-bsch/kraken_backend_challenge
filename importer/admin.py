from django.contrib import admin 

from importer.models import MeterReading

@admin.register(MeterReading) 
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = (  
        "mpan", 
        "meter_serial_number",  
        "register_id", 
        "reading_datetime",  
        "reading_value",
        "source_file",
    )  
    search_help_text = "Search by MPAN or meter serial number"  
    search_fields = (  
        "meter__meter_point__mpan",  
        "meter__serial_number", 
    ) 
    list_filter = ("register_id", "reading_datetime")  
    date_hierarchy = "reading_datetime"  
    ordering = ("-reading_datetime",) 
    list_select_related = ("meter", "meter__meter_point")  

    @admin.display(ordering="meter__meter_point__mpan", description="MPAN")  
    def mpan(self, obj):  
        return obj.meter.meter_point.mpan  

    @admin.display(ordering="meter__serial_number", description="Meter Serial")  
    def meter_serial_number(self, obj): 
        return obj.meter.serial_number  
