from .minio_service import MinioService
from ..models.image_model import Image


class ImageService:
    def __init__(self):
        pass

    def create(self, bucket_name: str, blob_name: str, blob, user_id):
        minio_service = MinioService()
        minio_service.create_bucket(bucket_name)
        minio_service.add_blob_to_bucket(bucket_name, blob, blob_name)
        data = {
            "bucket_name": bucket_name,
            "blob_name": blob_name,
        }
        image = Image.objects.create(**data, user_id=user_id)
        return image
    
    
    def get(self, id:int, user_id:int):
        try:
            image_object = Image.objects.get(id=id, user_id=user_id)
            minio_service = MinioService()
            blob = minio_service.get_blob_from_bucket(image_object.bucket_name, image_object.blob_name)
            data = blob.read()
            blob.close()
            blob.release_conn()
            return data
        except Image.DoesNotExist as e:
            raise e
    
    def delete(self, id:int, user_id:int):
        try:
            image_object = Image.objects.get(id=id, user_id=user_id)
            minio_service = MinioService()
            minio_service.remove_blob_from_bucket(image_object.bucket_name, image_object.blob_name)
        except Image.DoesNotExist as e:
            raise e
    
    def update(self):
        pass