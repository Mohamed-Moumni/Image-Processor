from rest_framework import serializers
from ..models.image_model import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "bucket_name", "blob_name"]