import os
import uuid

import pytest

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.urls import reverse

from core.models import File


@pytest.fixture
def user():
    user = User.objects.create_user(username='testuser', password='password')
    return user


@pytest.fixture
def file_instance(request):
    test_dir = os.path.join(settings.MEDIA_ROOT, 'test_files')

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    file_path = os.path.join(test_dir, 'test_file.txt')
    file_content = b'This is a test file'

    with default_storage.open(file_path, 'wb') as f:
        f.write(file_content)

    file_instance = File.objects.create(
        uuid=uuid.uuid4(),
        title='Test File',
        file=file_path,
    )

    def delete_test_files():
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(test_dir) and not os.listdir(test_dir):
            os.rmdir(test_dir)

    request.addfinalizer(delete_test_files)

    return file_instance


@pytest.mark.django_db
def test_download_file_authenticated(client, user, file_instance):
    client.login(username='testuser', password='password')
    url = reverse('download_file', args=[file_instance.uuid])
    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Disposition'] == 'attachment; filename="test_file.txt"'


@pytest.mark.django_db
def test_download_file_not_authenticated(client, file_instance):
    url = reverse('download_file', args=[file_instance.uuid])
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/?next=')
