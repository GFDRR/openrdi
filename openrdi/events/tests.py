"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

import os
from django.test import TestCase
from django.conf import settings
from geonode.maps.utils import file_upload
from openrdi.events.models import Event

TEST_DATA = os.path.join(settings.PROJECT_ROOT, 'events', 'data')
LOGIN_URL=settings.SITEURL + "accounts/login/"


class EventsTest(TestCase):
    fixtures = ['user',]

    def test_file_upload(self):
        """
        Tests that a file can be uploaded and associated with an specific event.
        """
        event, __ = Event.objects.get_or_create(id=1,
                        defaults=dict(name='rdrp', domain='rdrp.org', slug='rdrp'))
        thefile = os.path.join(TEST_DATA, 'KEN_Affected_Regions.shp')
        uploaded = file_upload(thefile, workspace=event.slug, overwrite=True)
        
        self.assertEqual(event.slug, uploaded.workspace)
