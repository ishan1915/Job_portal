from rest_framework import serializers

class Sort(serializers.Serializer):
    numbers = serializers.ListField(
        child = serializers.IntegerField(), allow_empty=False
    )