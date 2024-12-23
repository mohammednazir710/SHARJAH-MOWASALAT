from django.db import models
from datetime import datetime, timedelta

# Create your models here.

class BusStop(models.Model):
    name = models.CharField(max_length=255)  # Name of the stop
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)  # Unique code for the stop
    latitude = models.FloatField()  # Latitude of the stop
    longitude = models.FloatField()  # Longitude of the stop

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=255)  # Name or number of the route
    start_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name="starting_routes")  # Start stop
    end_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name="ending_routes")  # End stop

    def __str__(self):
        return f"Route: {self.name}"

    def total_stops(self):
        return self.route_stops.count()


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_stops")  # Associated route
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name="stop_routes")  # Associated stop
    order = models.PositiveIntegerField()  # Sequence order of the stop in the route

    class Meta:
        unique_together = ("route", "stop")  # Ensure no duplicate stop-route pairs
        ordering = ["order"]  # Default order by sequence

    def __str__(self):
        return f"{self.route.name} - Stop {self.order}: {self.stop.name}"


class BusSchedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="schedules")  # Route for the schedule
    reverse = models.BooleanField(default=False)
    dispatch_time = models.TimeField()  # Dispatch time
    arrival_time = models.TimeField()  # Arrival time

    def __str__(self):
        return f"Schedule for {self.route.name}: {self.dispatch_time} - {self.arrival_time}"
    
    def travel_duration(self):
        # Convert dispatch and arrival times to datetime objects
        dispatch_dt = datetime.combine(datetime.today(), self.dispatch_time)
        arrival_dt = datetime.combine(datetime.today(), self.arrival_time)

        # Adjust for overnight trips (arrival on the next day)
        if arrival_dt < dispatch_dt:
            arrival_dt += timedelta(days=1)

        # Calculate the duration
        duration = arrival_dt - dispatch_dt
        return int(duration.total_seconds() // 60)


class History(models.Model):
    key = models.CharField(max_length=100, blank=True, null=True)
    start = models.CharField(max_length=50, blank=True, null=True)
    end = models.CharField(max_length=50, blank=True, null=True)
    start_loc_name = models.CharField(max_length=255, blank=True, null=True)
    end_loc_name = models.CharField(max_length=255, blank=True, null=True)
    distance = models.FloatField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
