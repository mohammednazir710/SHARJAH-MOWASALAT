from django.db import models

# Create your models here.

class BusStop(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    lng = models.CharField(max_length=50, blank=True, null=True)
    start = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class EndStop(models.Model):
    from_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='from_stop')
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name="end_stop")
    
    def __str__(self):
        return f"{self.from_stop.code} to {self.stop.code}"
    
class BusSchedule(models.Model):
    end_stop = models.ForeignKey(EndStop, on_delete=models.CASCADE)
    dispatch = models.TimeField()
    arrival = models.TimeField()

    def __str__(self):
        return f"{self.end_stop}"