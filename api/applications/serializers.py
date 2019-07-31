from rest_framework import serializers
from .models import Application, Good

class ApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    date = serializers.DateTimeField(read_only=True)
    destination = serializers.CharField(max_length=200)
    goods = serializers.StringRelatedField(many=True, required=False)

    def create(self, validated_data):
        return Application.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.save()
        return instance

class GoodSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)

    def create(self, validated_data):
        return Good.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
