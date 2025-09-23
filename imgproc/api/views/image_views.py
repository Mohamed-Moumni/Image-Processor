from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.image_service import ImageService
from ..serializers.image_serializer import ImageSerializer


class ImageListView(APIView):
    def post(self, request):
        if not "image_uploaded" in request.FILES:
            return Response(
                {"from-data": {"image_uploaded": "field required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            image_bytes = request.FILES["image_uploaded"]
            image_service = ImageService()
            created_image = image_service.create(
                request.user.username, image_bytes.name, image_bytes, request.user.id
            )
            return Response(
                data=created_image,
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id: int = None):
        try:
            image_service = ImageService()
            data_img = image_service.get(id=id)
            return Response({"id": id, "username": request.user.username, **data_img}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"No Image Found with ID: {id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, id: int = None):
        try:
            image_service = ImageService()
            image_service.delete(id=id)
            return Response(
                {"message": f"Image with ID: {id} Deleted successfully."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"message": f"No Image Found with ID: {id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
