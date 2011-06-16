import datetime

from django.db.models.query import QuerySet, ValuesQuerySet
from django.http import HttpResponse
from geonode.maps.models import Layer, Contact, Role, ContactRole
import csv, StringIO

CONTACT_FIELDS = (
                  'id', 'name', 'organization', 'position', 'voice', 'fax',
                   'delivery', 'city', 'area', 'zipcode', 'country', 'email',
                    )

LAYER_FIELDS = (
              'id', 'name', 'title',
              'date', 'date_type', 'edition', 
              'abstract', #FIXME: Remove this one.
              'abstract_en', 'abstract_fr',
              'purpose_en', 'purpose_fr',
              'maintenance_frequency',
              'keywords', 'keywords_region',
              'constraints_use',
              'constraints_other_en', 'constraints_other_fr',
              'spatial_representation_type',
              'language',
              'topic_category',
              'temporal_extent_start',
              'temporal_extent_end',
              'supplemental_information_en', 'supplemental_information_fr',
              'distribution_url',
              'distribution_description_en', 'distribution_description_fr',
              'data_quality_statement_en', 'data_quality_statement_fr',
             )


def add_contact_info(layer, role):
    """Queries the contact role table and adds the contact fields
       to the given layer dictionary
    """

    contact = ContactRole.objects.get(role=role, layer__id = layer['id']).contact
    for field in CONTACT_FIELDS:
        layer['%s__%s' % (role.value, field)] = getattr(contact, field)
    return layer

def metadata(request, layer_list=None):
    """Returns a excel file with all the layers
    """
    layers = Layer.objects.all()

    if layer_list is not None:
        int_layer_list = [int(x) for x in layer_list.split(',')]
        layers = layers.filter(id__in=int_layer_list)

    objs = layers.values(*LAYER_FIELDS).order_by('typename')

    # Iterate over the list to annotate it with poc data and metadata_author data
    pocrole =  Role.objects.get(value='pointOfContact')
    authorrole = Role.objects.get(value='author')

    annotated_objects = []
    for layer in objs:
        layer = add_contact_info(layer, pocrole)
        layer = add_contact_info(layer, authorrole)
        annotated_objects.append(layer)

    response = HttpResponse(mimetype='text/csv')
    sd = datetime.datetime.now()
    fname = '%s-%s.csv' % ('layers', sd.strftime('%Y%m%d-%H%M-%s'))
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
     
    header = []
    header.extend(LAYER_FIELDS)
    for contact in ['pointOfContact', 'author']:
        for field in CONTACT_FIELDS:
            header.append('%s__%s' % (contact, field))


    writer = UnicodeDictWriter(response, header)
    header_writer = UnicodeWriter(response)
    header_writer.writerows([header])

    writer.writerows(annotated_objects)

    response._is_string = False
    return response




class UnicodeWriter(object):
    """
    Like UnicodeDictWriter, but takes lists rather than dictionaries.
    
    Usage example:
    
    fp = open('my-file.csv', 'wb')
    writer = UnicodeWriter(fp)
    writer.writerows([
        [u'Bob', 22, 7],
        [u'Sue', 28, 6],
        [u'Ben', 31, 8],
        # \xc3\x80 is LATIN CAPITAL LETTER A WITH MACRON
        ['\xc4\x80dam'.decode('utf8'), 11, 4],
    ])
    fp.close()
    """
    def __init__(self, f, dialect=csv.excel_tab, encoding="utf-16", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoding = encoding
    
    def writerow(self, row):
        # Modified from original: now using unicode(s) to deal with e.g. ints
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = data.encode(self.encoding)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class UnicodeDictWriter(UnicodeWriter):
    """
    A CSV writer that produces Excel-compatibly CSV files from unicode data.
    Uses UTF-16 and tabs as delimeters - it turns out this is the only way to
    get unicode data in to Excel using CSV.
    
    Usage example:
    
    fp = open('my-file.csv', 'wb')
    writer = UnicodeDictWriter(fp, ['name', 'age', 'shoesize'])
    writer.writerows([
        {'name': u'Bob', 'age': 22, 'shoesize': 7},
        {'name': u'Sue', 'age': 28, 'shoesize': 6},
        {'name': u'Ben', 'age': 31, 'shoesize': 8},
        # \xc3\x80 is LATIN CAPITAL LETTER A WITH MACRON
        {'name': '\xc4\x80dam'.decode('utf8'), 'age': 11, 'shoesize': 4},
    ])
    fp.close()
    
    Initially derived from http://docs.python.org/lib/csv-examples.html
    """
    
    def __init__(self, f, fields, dialect=csv.excel_tab,
            encoding="utf-16", **kwds):
        super(UnicodeDictWriter, self).__init__(f, dialect, encoding, **kwds)
        self.fields = fields
    
    def writerow(self, drow):
        row = [drow.get(field, '') for field in self.fields]
        super(UnicodeDictWriter, self).writerow(row)
