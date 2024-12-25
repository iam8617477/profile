import os
import psutil
import socket
import pwd

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .models import File


@login_required
def download_file(request, file_uuid):
    file_instance = get_object_or_404(File, uuid=file_uuid)
    file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)

    if not os.path.exists(file_path):
        raise Http404('File does not exist')

    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                yield chunk

    file_name = os.path.basename(file_path)
    response = StreamingHttpResponse(file_iterator(file_path), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


@login_required
def system_info(request):
    cpu_count = psutil.cpu_count(logical=True)
    cpu_percent = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    total_ram = round(memory.total / (1024 ** 3), 2)
    available_ram = round(memory.available / (1024 ** 3), 2)

    disk = psutil.disk_usage('/')
    total_disk = round(disk.total / (1024 ** 3), 2)
    free_disk = round(disk.free / (1024 ** 3), 2)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    users = [user.pw_name for user in pwd.getpwall() if user.pw_uid >= 1000]

    data = {
        'cpu_count': cpu_count,
        'cpu_percent': cpu_percent,
        'total_ram': total_ram,
        'available_ram': available_ram,
        'total_disk': total_disk,
        'free_disk': free_disk,
        'hostname': hostname,
        'ip_address': ip_address,
        'users': users,
    }

    return JsonResponse(data)
