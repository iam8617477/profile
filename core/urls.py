from django.urls import path
from . import views

urlpatterns = [
    path('download/<uuid:file_uuid>/', views.download_file, name='download_file'),
    path('system-info/', views.system_info, name='system_info'),
]
