from rest_framework.views import APIView
from ..services.transformation_service import TransformationService, ImageService
from ..serializers.transformation_serializer import ChangeFormatTransformationSerializer, CompressTransformationSerializer, FlipTransformationSerializer, RotateTransformationSerializer, CropTransformationSerializer, ResizeTransformationSerializer
from rest_framework.response import Response
from rest_framework import status

class TransformationResizeView(APIView):
    def post(self, request, id:int):
        serializer = ResizeTransformationSerializer(data=request.data)
        if serializer.is_valid():
            trans_service = TransformationService()
            img_serv = ImageService()
            image = img_serv.get(id)
            transformed_image = trans_service.resize(image, **serializer.validated_data)
            return Response(data=transformed_image, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransformationCropView(APIView):
    def post(self, request, id:int):
        serializer = CropTransformationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                trans_service = TransformationService()
                img_serv = ImageService()
                image = img_serv.get(id)
                transformed_image = trans_service.crop(image, **serializer.validated_data)
                return Response(data=transformed_image, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransformationRotateView(APIView):
    def post(self, request, id:int):
        serializer = RotateTransformationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                trans_service = TransformationService()
                img_serv = ImageService()
                image = img_serv.get(id)
                transformed_image = trans_service.rotate(image, **serializer.validated_data)
                return Response(data=transformed_image, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransformationFlipView(APIView):
    def post(self, request, id:int):
        serializer = FlipTransformationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                trans_service = TransformationService()
                img_serv = ImageService()
                image = img_serv.get(id)
                transformed_image = trans_service.flip(image, **serializer.validated_data)
                return Response(data=transformed_image, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransformationCompressView(APIView):
    def post(self, request, id:int):
        serializer = CompressTransformationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                trans_service = TransformationService()
                img_serv = ImageService()
                image = img_serv.get(id)
                transformed_image = trans_service.compress(image, **serializer.validated_data)
                return Response(data=transformed_image, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransformationChangeFormatView(APIView):
    def post(self, request, id:int):
        serializer = ChangeFormatTransformationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                trans_service = TransformationService()
                img_serv = ImageService()
                image = img_serv.get(id)
                transformed_image = trans_service.change_format(image, request.user.id, **serializer.validated_data,)
                return Response(data=transformed_image, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)