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
