from django.urls import path
from zipdir import views
from zipdir.views import CreateArchiveView,  ArchiveStatus

urlpatterns = [
    path('api/archive/create/', CreateArchiveView.as_view(), name='create_archive'),
    path('api/archive/status/<str:task_id>', ArchiveStatus.as_view(), name = 'archive_status'),
]









