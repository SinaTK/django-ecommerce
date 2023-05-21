from bucket import bucket
from celery import shared_task


# TODO: can be async?
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result

@shared_task
def delete_bucket_object_task(key):
    bucket.delete_object(key)

@shared_task
def download_bucket_object_task(key):
    bucket.download_object(key)

@shared_task
def upload_bucket_object_task(file_name, bucket_file_name):
    bucket.upload_object(file_name=file_name, bucket_file_name=bucket_file_name)