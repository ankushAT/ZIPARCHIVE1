import os
import shutil
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from zipArchive.celery import app
from celery.result import AsyncResult
from .tasks import create_archive


def check_status(task_id):
    archive_path = 'archives/{}.zip'.format(task_id)
    task = AsyncResult(task_id)
    status = task.status
    if status == "SUCCESS":
        # archive_hash = task.result
        # _, url = check_status(archive_hash)
        return 'Completed', archive_path
    else:
        return 'in-progress', None
        


class CreateArchiveView(APIView):

    def post(self, request):
        urls = request.data.get('urls',[])
        if not urls:
            return Response({"error": "No URLs provided"}, status=status.HTTP_400_BAD_REQUEST)        
        task = create_archive.delay(urls)
        return Response({"Task Id :", task.id})


class ArchiveStatus(APIView):
    def get(self, request):
        task_id = request.data['task_id']
        status, url = check_status(task_id)
        return Response({'status': status, 'url': url})




class DownloadZipFile(APIView):

    def get(self, request):
        # breakpoint()
        archive_path = request.data['file_path']
        task_id = archive_path.split("/")[-1].replace(".zip", "")
        if os.path.exists(archive_path):
            with open(archive_path, 'rb') as f:
                response = HttpResponse(f, content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{task_id}.zip"'
                response.content = b"File downloaded successfully"
                return response
        else:
            return Response({"error": "Archive not found"}, status=status.HTTP_404_NOT_FOUND)


class DownloadZipFile(APIView):
    def get(self, request):
        archive_path = request.data['file_path']
        task_id = archive_path.split("/")[-1].replace(".zip", "")
        download_folder = 'download'
        if not os.path.exists(download_folder):
            os.mkdir(download_folder)
        elif not os.path.isdir(download_folder):
            return Response({"error": "Download folder path exists but is not a folder"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        download_path = os.path.join(download_folder, f"{task_id}.zip")
        if os.path.exists(download_path):
            return Response({"error": "File already downloaded"}, status=status.HTTP_400_BAD_REQUEST)                
        elif os.path.exists(archive_path):    
            download_path = os.path.join("download/", f"{task_id}.zip")
            with open(archive_path, 'rb') as f:
                with open(download_path, 'wb') as downloaded_file:
                    shutil.copyfileobj(f, downloaded_file)
                with open(download_path, 'rb') as downloaded_file:
                    response = HttpResponse(downloaded_file, content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename="{task_id}.zip"'
                    response.content = b"File downloaded successfully"
                    return response
        else:
            return Response({"error": "Archive not found"}, status=status.HTTP_404_NOT_FOUND)
        

