from rest_framework import serializers

class ResizeTransformationSerializer(serializers.Serializer):
    FIT_TYPES = [
        ('cover', 'Cover'),
        ('contain', 'Contain'),
        ('fill', 'Fill')
    ]
    width = serializers.FloatField()
    height = serializers.FloatField()
    fit = serializers.ChoiceField(choices=FIT_TYPES, default='cover')
    upscale = serializers.BooleanField(default=False)
    background = serializers.CharField(default="#ffffff")