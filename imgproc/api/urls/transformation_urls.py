from django.urls import path
from ..views.transformation_views import TransformationRotateView, TransformationResizeView, TransformationCropView

urlpatterns = [
    path("resize/<int:id>", TransformationResizeView.as_view(), name="resize_transformation_view"),
    path("crop/<int:id>", TransformationCropView.as_view(), name="crop_transformation_view"),
    path("rotate/<int:id>", TransformationRotateView.as_view(), name="rotate_transformation_view")
]