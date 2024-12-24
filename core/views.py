import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import File


@login_required
def download_file(request, file_uuid):
    file_instance = get_object_or_404(File, uuid=file_uuid)
    file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)

    if not os.path.exists(file_path):
        raise Http404('File does not exist')

    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
