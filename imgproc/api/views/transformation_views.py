from rest_framework.views import APIView
from ..services.transformation_service import TransformationService
from ..serializers.transformation_serializer import ResizeTransformationSerializer
from rest_framework.response import Response
from rest_framework import status

class TransformationResizeView(APIView):
    def post(self, request, id:int):
        serializer = ResizeTransformationSerializer(data=request.data)
        if serializer.is_valid():
            trans_service = TransformationService()
            image = trans_service.resize(id, **serializer.validated_data)
            return Response(data=image, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)