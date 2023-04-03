from django.urls import path
from zipdir import views
from zipdir.views import CreateArchiveView,  ArchiveStatus, DownloadZipFile

urlpatterns = [
    path('api/archive/create/', CreateArchiveView.as_view(), name='create_archive'),
    path('api/archive/status/', ArchiveStatus.as_view(), name = 'archive_status'),
    path('archive/get/', DownloadZipFile.as_view(), name = 'download_zipfile'),

]









