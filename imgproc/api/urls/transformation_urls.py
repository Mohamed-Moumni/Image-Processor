from django.urls import path
from ..views.transformation_views import TransformationResizeView

urlpatterns = [
    path("<int:id>", TransformationResizeView.as_view(), name="resize_transformation_view")
]