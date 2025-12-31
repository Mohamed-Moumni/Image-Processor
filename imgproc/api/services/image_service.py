from .minio_service import MinioService
from ..models.image_model import Image
from ..serializers.image_serializer import ImageSerializer


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
        serializer = ImageSerializer(image)
        return serializer.data
    
    
    def get(self, id:int):
        try:
            image_object = Image.objects.get(id=id)
            minio_service = MinioService()
            blob_url = minio_service.get_blob_from_bucket(image_object.bucket_name, image_object.blob_name)
            serializer = ImageSerializer(image_object)
            data = {
                **(serializer.data),
                "image_url": blob_url,
            }
            return data
        except Image.DoesNotExist as e:
            raise e
    
    def delete(self, id:int):
        try:
            image_object = Image.objects.get(id=id)
            minio_service = MinioService()
            minio_service.remove_blob_from_bucket(image_object.bucket_name, image_object.blob_name)
            image_object.delete()
        except Image.DoesNotExist as e:
            raise e
    
    def update(self):
        pass