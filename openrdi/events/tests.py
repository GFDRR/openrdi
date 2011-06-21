"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

import os
from django.test import TestCase
from django.conf import settings
from geonode.maps.utils import file_upload
from geonode.maps.models import Map, Layer
from openrdi.events.models import Event, EventMap
from django.test.client import Client

TEST_DATA = os.path.join(settings.PROJECT_ROOT, 'events', 'data')
LOGIN_URL=settings.SITEURL + "accounts/login/"

def get_event():
    event, __ = Event.objects.get_or_create(id=1,
                    defaults=dict(name='rdrp', domain='rdrp.org', slug='rdrp'))
    return event

class EventsTest(TestCase):
    fixtures = ['user',]

    def setUp(self):
        self.event = get_event()

    def test_event_file_upload(self):
        """
        Tests that a file can be uploaded and associated with an specific event.
        """
        thefile = os.path.join(TEST_DATA, 'KEN_Affected_Regions.shp')
        uploaded = file_upload(thefile, workspace=self.event.slug, overwrite=True)
        
        self.assertEqual(self.event.slug, uploaded.workspace)

    def test_file_upload(self):
        """
        Tests that a file can be uploaded without associating it with an specific event.
        """
        thefile = os.path.join(TEST_DATA, 'TM_WORLD.shp')
        uploaded = file_upload(thefile, overwrite=True)
        assert uploaded.typename is not None

    def test_event_list(self):
        """
        Tests that the event is listed
        """
        c = Client()
        response = c.get('/events/')
        events = response.context['object_list']
        assert self.event in events
        self.assertContains(response, self.event.name)

    def test_event_detail(self):
        """
        Test that the detail page contains all the maps and layers associated with it
        """
        c = Client()
        response = c.get('/events/%s' % self.event.slug)
        self.assertContains(response, self.event.name)
        layers = Layer.objects.get(workspace=self.event.slug)
        for layer in layers:
            self.assertContains(response, title)
