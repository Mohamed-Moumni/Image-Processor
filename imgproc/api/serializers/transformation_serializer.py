from rest_framework import serializers

class ResizeTransformationSerializer(serializers.Serializer):
    FIT_TYPES = [
        ('cover', 'Cover'),
        ('contain', 'Contain'),
        ('fill', 'Fill')
    ]
    width = serializers.FloatField(required=True)
    height = serializers.FloatField(required=True)
    fit = serializers.ChoiceField(choices=FIT_TYPES, default='cover')
    upscale = serializers.BooleanField(default=False)
    background = serializers.CharField(default="#ffffff")

class CropTransformationSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    width = serializers.FloatField()
    height = serializers.FloatField()

class RotateTransformationSerializer(serializers.Serializer):
    angle = serializers.FloatField()
    background_color = serializers.CharField(default="#ffffff")
    auto_orient = serializers.IntegerField(required=False)

class FlipTransformationSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(
        choices=["horizontal", "vertical"],
        help_text="Flip direction: 'horizontal' (left-right) or 'vertical' (top-bottom)")

class CompressTransformationSerializer(serializers.Serializer):
    quality = serializers.IntegerField(
        min_value=1,
        max_value=100,
        help_text="Compression quality level (1–100)"
    )
    method = serializers.ChoiceField(
        choices=["lossy", "lossless", "progressive"],
        help_text="Compression method"
    )
    optimize = serializers.BooleanField(
        default=False,
        help_text="Auto-tune compression"
    )
    strip_metadata = serializers.BooleanField(
        default=False,
        help_text="Remove EXIF/IPTC metadata"
    )

class ChangeFormatTransformationSerializer(serializers.Serializer):
    FORMAT_CHOICES = ["jpeg", "png", "webp", "avif", "gif"]

    format = serializers.ChoiceField(
        choices=FORMAT_CHOICES,
        help_text="Target image format"
    )
    quality = serializers.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        help_text="Optional quality (if supported by the format)"
    )
    background = serializers.CharField(
        default="#ffffff",
        help_text="Background fill for non-transparent formats like JPEG"
    )

class FilterTransformationSerializer(serializers.Serializer):
    FILTER_CHOICES = [
        "grayscale",
        "sepia",
        "blur",
        "brightness",
        "contrast",
        "sharpen",
        "edge",
    ]

    filter_type = serializers.ChoiceField(
        choices=FILTER_CHOICES,
        help_text="Type of filter to apply"
    )
    intensity = serializers.FloatField(
        required=False,
        default=1.0,
        help_text="Filter strength (0–100 or float depending on filter)"
    )
    radius = serializers.FloatField(
        required=False,
        help_text="Optional radius (used for blur, edge detection)"
    )
    threshold = serializers.IntegerField(
        required=False,
        help_text="Optional threshold for edge/contrast filters"
    )