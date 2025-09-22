from django.urls import path
from ..views.user_views import UserListView, UserAuthView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("logout", UserAuthView.as_view(), name="user_auth"),
    path("register", UserListView.as_view(), name="user_list"),
    path("<int:id>", UserListView.as_view(), name="user_list"),
    path("<str:username>", UserListView.as_view(), name="user_list"),
]
