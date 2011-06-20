# Create your views here.
"""
from geonode.maps.forms import NewLayerUploadForm
from geonode.maps.utils import save
from django.utils.html import escape
import os, shutil
 
class EventLayerUploadForm(NewLayerUploadForm):
    event = 

@login_required
@csrf_exempt
def upload_layer(request):
    if request.method == 'GET':
        return render_to_response('maps/layer_upload.html',
                                  RequestContext(request, {}))
    elif request.method == 'POST':
        form = NewLayerUploadForm(request.POST, request.FILES)
        tempdir = None
        if form.is_valid():
            try:
                tempdir, base_file = form.write_files()
                name, __ = os.path.splitext(form.cleaned_data["base_file"].name)
                saved_layer = save(name, base_file, request.user,
                        overwrite = False,
                        abstract = form.cleaned_data["abstract"],
                        title = form.cleaned_data["layer_title"],
                        permissions = form.cleaned_data["permissions"]
                        )
                return HttpResponse(json.dumps({
                    "success": True,
                    "redirect_to": saved_layer.get_absolute_url() + "?describe"}))
            except Exception, e:
                logger.exception("Unexpected error during upload.")
                return HttpResponse(json.dumps({
                    "success": False,
                    "errors": ["Unexpected error during upload: " + escape(str(e))]}))
            finally:
                if tempdir is not None:
                    shutil.rmtree(tempdir)
        else:
            errors = []
            for e in form.errors.values():
                errors.extend([escape(v) for v in e])
            return HttpResponse(json.dumps({ "success": False, "errors": errors}))
"""
