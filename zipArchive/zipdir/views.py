import os
from django.http import FileResponse
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from zipArchive.celery import app
from celery.result import AsyncResult
from .tasks import create_archive
from django.urls import reverse

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
    def get(self, request, task_id):
        status, url = check_status(task_id)
        if status == 'Completed':
            download_url = os.path.join("localhost:8000",url)
        else:
            download_url = None

        return Response({'status': status, 'download_url': download_url})