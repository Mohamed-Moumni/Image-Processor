from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    bucket_name = models.CharField(max_length=100)
    blob_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bucket_name}-{self.blob_name}"