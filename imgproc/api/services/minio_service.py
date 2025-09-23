import os
from datetime import timedelta
from minio import Minio

class MinioService:
    def __init__(self):
        access_key = os.getenv("MINIO_ROOT_USER")
        secret_key = os.getenv("MINIO_ROOT_PASSWORD")
        minio_host = os.getenv("MINIO_HOST")
        if not access_key or not secret_key or not minio_host:
            raise ValueError("Invalid Minio Credentials")
        self.instance = Minio(minio_host,secure=False, access_key=access_key, secret_key=secret_key)

    def create_bucket(self, bucket_name:str) -> bool:
        if not self.instance.bucket_exists(bucket_name):
            bucket = self.instance.make_bucket(bucket_name)
        return True

    def add_blob_to_bucket(self, bucket_name: str, blob, blob_name:str) -> bool:
        length = len(blob.read())
        blob.seek(0)
        self.instance.put_object(bucket_name, blob_name, blob, length)
        return blob_name

    def remove_blob_from_bucket(self, bucket_name:str, blob_name:str):
        self.instance.remove_object(bucket_name, blob_name)

    def get_blob_from_bucket(self, bucket_name:str, blob_name:str):
        return self.instance.presigned_get_object(bucket_name, blob_name, expires=timedelta(minutes=30))
    
    def blob_exist_in_bucket(self, bucket_name:str, blob_name:str) -> bool:
        try:
            self.instance.get_object(bucket_name, blob_name)
            return True
        except Exception as e:
            return False


    # def update_blob(self):
    #     pass