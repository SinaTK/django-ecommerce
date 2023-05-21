from django.conf import settings
from boto3 import session


class Bucket:
    '''CDN bucket manager

    init create connection.
    '''

    def __init__(self):
        sess = session.Session()
        self.conn = sess.client(
            service_name= settings.AWS_SERVICE_NAME,
            aws_access_key_id= settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def get_objects(self):
        objects = self.conn.list_objects_v2(Bucket=self.bucket_name)
        if objects['Contents']:
            return objects['Contents']
        else:
            return None

    def delete_object(self, key):
        self.conn.delete_object(Bucket=self.bucket_name, Key=key)
        return True
    
    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.conn.download_fileobj(self.bucket_name, key, f)
        return True
    
    def upload_object(self, file_name, bucket_file_name):
        self.conn.upload_file(file_name, self.bucket_name, bucket_file_name)
        return True
bucket = Bucket()