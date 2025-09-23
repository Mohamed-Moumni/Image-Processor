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
        image_bytes = request.FILES["image_uploaded"]
        image_service = ImageService()
        created_image = image_service.create(
            request.user.username, image_bytes.name, image_bytes, request.user.id
        )
        serializer = ImageSerializer(data=created_image)
        if serializer.is_valid():
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id: int = None, user_id: int = None):
        try:
            if id and user_id:
                image_service = ImageService()
                data_img = image_service.get(id, user_id=user_id)
                return Response(data=data_img, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"No Image Found with ID: {id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, id: int = None, user_id: int = None):
        try:
            if id and user_id:
                image_service = ImageService()
                image_service.delete(id=id, user_id=user_id)
                return Response(
                    {"message": f"Image with ID: {id} Deleted successfully."}
                )
        except Exception as e:
            return Response(
                {"message": f"No Image Found with ID: {id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
