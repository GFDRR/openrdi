from django.contrib import admin
from openrdi.events.models import Event, Colors, EventMap

class MapInline(admin.TabularInline):
    model = EventMap

class EventAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'center_lat', 'center_lon', 'zoom',)
    inlines =[
        MapInline,
    ]

admin.site.register(Event, EventAdmin)
admin.site.register(Colors)
admin.site.register(EventMap)
