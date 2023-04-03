from time import sleep
from zipArchive.celery import app
import requests
import os
import hashlib
import zipfile
from celery.contrib import rdb
from celery import shared_task
import urllib.parse
import tempfile

VIDEO_EXTENSIONS = ['.mp4', '.mov', '.wmv', '.avi', '.avchd', '.flv', '.f4v', '.swf', '.mkv', '.webm']


@shared_task
def create_archive(urls):
    rdb.set_trace() 
    task_id = create_archive.request.id
    archive_path = 'archives/{}.zip'.format(task_id)
    print("Archive Path", archive_path)
    if not os.path.exists('archives'):
        os.makedirs('archives')
    try:
        with zipfile.ZipFile(archive_path, 'w') as archive:
            for url in urls:    
                if any(url.endswith(ext) for ext in VIDEO_EXTENSIONS):
                    response = requests.get(url)
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(response.content)
                        tmp_file.flush()                
                        file_name = os.path.basename(url)
                        archive.writestr(file_name, response.content)
                    os.unlink(tmp_file.name)
                else:
                    response = requests.get(url)
                    file_name = os.path.basename(url)
                    archive.writestr(file_name, response.content)

    except Exception as e:
        print(f"Error creating archive: {e}")
        return None

    return archive_path 
