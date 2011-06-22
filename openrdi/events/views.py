from geonode.maps.views import upload_layer

def upload(request, slug):
   """Wrapper around GeoNode's upload_layer view to enable workspaces.
   """
   return upload_layer(request, template='events/upload.html', workspace=slug)
