from time import sleep
from zipArchive.celery import app
import requests
import os
import hashlib
import zipfile
from celery.contrib import rdb
from celery import shared_task

@shared_task
def test_func():
    # rdb.set_trace()
    for i in range(10):
        print(i)
    return "DONE"


@shared_task
def create_archive(urls):
    rdb.set_trace()
    print("kfmvkfkvm")
    archive_path = 'archives/{}.zip'.format(task.id)
    print("This is the archive path", archive_path)
    with zipfile.ZipFile(archive_path, 'w') as archive:
        for url in urls:
            response = requests.get(url)
            file_name = os.path.basename(url)
            archive.writestr(file_name, response.content)
    return archive_path

