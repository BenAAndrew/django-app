from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import Good


class GoodSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200, validators=[RegexValidator("^[^(0-9)]*$", message="Please don't enter numbers", code="includesNumbers")])

    def create(self, validated_data):
        return Good.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
