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