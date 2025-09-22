from rest_framework import serializers
from models.image_model import Image

class ImageUpload(serializers.ModelSerializer):
    image_uploaded = serializers.FileField()

    class Meta:
        fields = ['image_uploaded']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["bucket_name", "blob_name"]