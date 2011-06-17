from django.conf.urls.defaults import *
from openrdi.events.models import Event

info_dict = {
    'queryset': Event.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list',
            info_dict, 'event-list'),
    (r'^(?P<slug>\w+)/$', 'django.views.generic.list_detail.object_detail',
            info_dict, 'event-detail'),
)
