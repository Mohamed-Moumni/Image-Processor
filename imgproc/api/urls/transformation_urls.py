from django.urls import path
from ..views.transformation_views import TransformationCompressView, TransformationRotateView, TransformationResizeView, TransformationCropView, TransformationFlipView

urlpatterns = [
    path("resize/<int:id>", TransformationResizeView.as_view(), name="resize_transformation_view"),
    path("crop/<int:id>", TransformationCropView.as_view(), name="crop_transformation_view"),
    path("rotate/<int:id>", TransformationRotateView.as_view(), name="rotate_transformation_view"),
    path("flip/<int:id>", TransformationFlipView.as_view(), name="flip_transformation_view"),
    path("compress/<int:id>", TransformationCompressView.as_view(), name="compress_transformation_view")
]