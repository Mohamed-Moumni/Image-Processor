from rest_framework.views import APIView
from ..serializers.user_serializer import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from ..services.user_services import UserService
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

class UserAuthView(APIView):
    """
        Auth User View
    """

    def post(self, request, format=None):
        try:
            if not 'refresh_token' in request.data:
                return Response(data={"refresh_token": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged Out!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    """
        List User View
    """

    def get_permissions(self):
        if not self.request.method in ["POST"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    @authentication_classes([AllowAny])
    @permission_classes([AllowAny])
    def post(self, request, format=None):
        try:
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_service = UserService()
                user = user_service.create(**user_serializer.data)
                return Response(data=user, status=status.HTTP_201_CREATED)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e
    
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, id:int=None, username:str=None, format=None):
        user_service = UserService()
        if id:
            try:
                user = user_service.get_by_id(id)
                return Response(data=user, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"The User with Id {id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if username:
            try:
                user = user_service.get_by_username(username)
                return Response(data=user, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"The User with Username {username} not found"}, status=status.HTTP_404_NOT_FOUND)