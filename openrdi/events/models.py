from django.db import models
from geonode.maps.models import Map



COLOR_HELPFIELD = 'Use "#FF33FF" or "black" '
class Colors(models.Model):
    name = models.CharField(max_length=255)
    crossbar_background = models.CharField(max_length=7, help_text=COLOR_HELPFIELD)
    crossbar_font = models.CharField(max_length=7, help_text=COLOR_HELPFIELD)
    hyperlink = models.CharField(max_length=7, help_text=COLOR_HELPFIELD)
    body_font = models.CharField(max_length=7, help_text=COLOR_HELPFIELD)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    banner = models.ImageField(upload_to='events', null=True, blank=True)
    logo = models.ImageField(upload_to='events', null=True, blank=True)
    featured = models.ManyToManyField(Map, null=True, blank=True)
    center_lat = models.FloatField(default = 0)
    center_lon = models.FloatField(default = 0)
    zoom = models.SmallIntegerField(default = 15)
    colors = models.ForeignKey(Colors, null=True, blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return('event-detail', None, {'slug': self.slug})
