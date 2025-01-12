import json
import os
import uuid

import pytest

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.urls import reverse

from core.models import AR, File


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


@pytest.mark.django_db
def test_non_get_request(client):
    ar_record = AR.objects.create(uuid='123e4567-e89b-12d3-a456-426614174000', data={})
    url = reverse('analyze_request', kwargs={'uuid': ar_record.uuid})
    response = client.post(url, data={'param1': 'value1'})

    assert response.status_code == 405


@pytest.mark.django_db
def test_get_request_with_existing_data(client):
    ar_record = AR.objects.create(uuid='123e4567-e89b-12d3-a456-426614174000', data={'existing': 'data'})
    url = reverse('analyze_request', kwargs={'uuid': ar_record.uuid})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_request_with_body(client):
    ar_record = AR.objects.create(uuid='123e4567-e89b-12d3-a456-426614174000', data={})
    url = reverse('analyze_request', kwargs={'uuid': ar_record.uuid})
    params = {'param1': 'value1', 'param2': 'value2'}
    body = {'key': 'value'}
    headers = {
        'Content-Type': 'application/json',
    }
    response = client.get(
        url + '?param1=value1&param2=value2', body=json.dumps(body), headers=headers, HTTP_CUSTOM_HEADER='header_value'
    )

    assert response.status_code == 200

    ar_record.refresh_from_db()
    assert ar_record.data['method'] == 'GET'
    assert ar_record.data['GET_params'] == params
    assert ar_record.data['content_type'] == 'application/json'

    assert 'HTTP_CUSTOM_HEADER' in ar_record.data['headers']
    assert ar_record.data['headers']['HTTP_CUSTOM_HEADER'] == 'header_value'
