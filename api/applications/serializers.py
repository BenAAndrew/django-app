from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import Application, Good


class ApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    date = serializers.DateTimeField(read_only=True)
    destination = serializers.CharField(max_length=200)
    progress = serializers.CharField(max_length=10, default='draft')
    goods = serializers.PrimaryKeyRelatedField(queryset=Good.objects.all(), many=True, required=True, allow_empty=False)

    def create(self, validated_data):
        goods = validated_data.pop('goods')
        application = Application.objects.create(**validated_data)
        application.goods.set(goods)
        return application

    def update(self, instance, validated_data):
        goods = validated_data.pop('goods')
        instance.name = validated_data.get('name', instance.name)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.progress = validated_data.get('progress', instance.progress)
        instance.save()
        instance.goods.set(goods)
        return instance


class GoodSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200, validators=[RegexValidator("^[^(0-9)]*$", message="Please don't enter numbers", code="includesNumbers")])

    def create(self, validated_data):
        return Good.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
