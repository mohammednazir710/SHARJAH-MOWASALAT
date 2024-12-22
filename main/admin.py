
from django.contrib import admin
from .models import BusStop, Route, RouteStop, BusSchedule

@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "code")
    search_fields = ("name", "code")

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("name", "start_stop", "end_stop")
    search_fields = ("name",)
    list_filter = ("start_stop", "end_stop")
    

@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ("route", "stop", "order")
    list_filter = ("route",)
    ordering = ("route", "order")
    autocomplete_fields = ['stop']

@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ("route", "dispatch_time", "arrival_time")
    list_filter = ("route",)
