from rest_framework.views import APIView
from ..serializers.user_serializer import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from ..services.user_services import UserService
from rest_framework.permissions import AllowAny

class UserListView(APIView):
    """
        List User View
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    
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