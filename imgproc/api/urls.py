from django.urls import path
from .views.user_views import UserListView

urlpatterns = [
    path("register", UserListView.as_view(), name="user_list"),
    path("<int:id>", UserListView.as_view(), name="user_list"),
    path("<str:username>", UserListView.as_view(), name="user_list")
]
