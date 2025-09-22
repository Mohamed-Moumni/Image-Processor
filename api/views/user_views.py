from rest_framework.views import APIView
from serializers import UserSerializer

class UserListView(APIView):
    """
        List User View
    """
    
    def post(self, request, format=None):
        user_serializer = UserSerializer()