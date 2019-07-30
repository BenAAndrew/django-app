from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    date = serializers.DateTimeField(read_only=True)
    destination = serializers.CharField(max_length=200)
    goods = serializers.StringRelatedField(many=True)

    def create(self, validated_data):
        return Application.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.title)
        instance.date = validated_data.get('date', instance.date)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.goods = validated_data.get('goods', instance.goods)
        instance.save()
        return instance
