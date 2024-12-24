from django.urls import path
from . import views

urlpatterns = [
    path('download/<uuid:file_uuid>/', views.download_file, name='download_file'),
]
