from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.image_service import ImageService
from django.contrib.auth.models import User


class ImageListView(APIView):
    def post(self, request):
        if not "image_uploaded" in request.FILES:
            return Response(
                {"from-data": {"image_uploaded": "field required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        image_bytes = request.FILES["image_uploaded"]
        image_service = ImageService()
        image_service.create(
            request.user.username, image_bytes.name, image_bytes, request.user.id
        )
        return Response(
            {"message": f"{image_bytes.name} uploaded successfully"},
            status=status.HTTP_201_CREATED,
        )
