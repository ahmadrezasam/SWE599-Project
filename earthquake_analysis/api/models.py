from django.db import models

class Earthquake(models.Model):
    event_id = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    origin_time = models.TimeField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    magnitude = models.FloatField(null=True, blank=True)
    md = models.FloatField(null=True, blank=True)
    ml = models.FloatField(null=True, blank=True)
    mw = models.FloatField(null=True, blank=True)
    ms = models.FloatField(null=True, blank=True)
    mb = models.FloatField(null=True, blank=True)
    event_type = models.CharField(max_length=10,null=True, blank=True)
    location = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.location