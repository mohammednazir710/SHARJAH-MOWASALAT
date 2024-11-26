from django.contrib import admin
from .models import BusStop, EndStop, BusSchedule, History
# Register your models here.
@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ['code','name', 'lat', 'lng']

admin.site.register(EndStop)
admin.site.register(BusSchedule)
admin.site.register(History)