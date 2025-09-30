from django.urls import path
from ..views.transformation_views import TransformationResizeView, TransformationCropView

urlpatterns = [
    path("resize/<int:id>", TransformationResizeView.as_view(), name="resize_transformation_view"),
    path("crop/<int:id>", TransformationCropView.as_view(), name="crop_transformation_view")
]