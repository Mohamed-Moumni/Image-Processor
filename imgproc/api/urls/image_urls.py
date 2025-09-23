from django.urls import path
from ..views.image_views import ImageListView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("upload", ImageListView.as_view(), name="image_list"),
    path("<int:id>", ImageListView.as_view(), name="image_list"),
]
