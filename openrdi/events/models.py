from django.db import models
from geonode.maps.models import Map

class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    banner = models.ImageField(upload_to='events', null=True, blank=True)
    logo = models.ImageField(upload_to='events', null=True, blank=True)
    featured = models.ManyToManyField(Map, null=True, blank=True)
    center_lat = models.FloatField(default = 0)
    center_lon = models.FloatField(default = 0)
    zoom = models.SmallIntegerField(default = 15)

    def __unicode__(self):
        return self.title
