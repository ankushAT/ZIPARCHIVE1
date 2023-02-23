from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from zipArchive.celery import app
from celery.result import AsyncResult
from .tasks import create_archive, test_func

def test(request):
    test_func.delay()
    return HttpResponse("DONE")


def check_status(task_id):
    archive_path = 'archives/{}.zip'.format(task_id)
    task = AsyncResult(task_id)
    status = task.status
    if status == "SUCCESS":
        archive_hash = task.result
        _, url = check_status(archive_hash)
        return 'Completed', archive_path
    else:
        return 'in-progress', None
        

# @app.task
# def create_archive(urls):
#     rdb.set_trace()
#     archive_path = 'archives/{}.zip'.format(task.id)
#     with zipfile.ZipFile(archive_path, 'w') as archive:
#         for url in urls:
#             response = requests.get(url)
#             file_name = os.path.basename(url)
#             archive.writestr(file_name, response.content)
#     return archive_path


class CreateArchiveView(APIView):

    def post(self, request):
        urls = request.data.get('urls',[])
        if not urls:
            return Response({"error": "No URLs provided"}, status=status.HTTP_400_BAD_REQUEST)
        import pdb;pdb.set_trace()     
        task = create_archive.delay(urls)
        return Response({"Task Id :", task.id})


class ArchiveStatus(APIView):
    def get(self, request):
        task_id = request.data['task_id']
        status, url = check_status(task_id)
        return Response({'status': status, 'url': url})


class DownloadZipFile(APIView):
    def get(self, request):
        archive_path = request.data['file_id']
        with open(archive_path, 'rb') as f:
            return Response(f.read(), content_type='application/zip')






























# response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(archive_path))            