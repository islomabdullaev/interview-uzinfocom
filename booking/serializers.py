from django.forms import ValidationError
from rest_framework import serializers

from booking.models import Playground, PlaygroundBooking, PlaygroundImageItem
from users.serializers import UserResponseSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status


class CreatePlaygroundImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaygroundImageItem
        fields = ["playground", "file"]


class PlaygroundImageResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaygroundImageItem
        fields = ["id", "playground", "file"]


class CreatePlaygroundSerializer(serializers.ModelSerializer):
    images = CreatePlaygroundImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    class Meta:
        model = Playground
        fields = [
            "name", "latitude", "longtitude", "price_per_hour", "phone_number",
            "images", "uploaded_images", "owner"]

    def create(self, validated_data):
        try:
            with transaction.atomic():
                uploaded_images = validated_data.pop("uploaded_images")
                playground = Playground.objects.create(**validated_data)
                for image in uploaded_images:
                    PlaygroundImageItem.objects.create(playground=playground, file=image)

                return True

        except Exception as e:
            print(e)

            return False



class PlaygroundResponseSerializer(serializers.ModelSerializer):
    images = PlaygroundImageResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Playground
        fields = ["id", "name", "latitude", "longtitude", "price_per_hour", "phone_number", "images"]


class PlaygroundBookingCreateSerializer(serializers.ModelSerializer):
    playground = serializers.UUIDField(write_only=True)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    for_date = serializers.DateField()

    class Meta:
        model = PlaygroundBooking
        fields = ["playground", "start_time", "end_time", "for_date"]



class PlaygroundBookingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    playground = PlaygroundResponseSerializer(read_only=True)
    user = UserResponseSerializer(read_only=True)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    for_date = serializers.DateField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = PlaygroundBooking
        fields = ["id", "playground", "user", "start_time", "end_time", "for_date", "status"]


class UpdatePlaygroundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playground
        fields = ['name', 'latitude', 'longtitude', 'price_per_hour', 'phone_number']

    def update(self, instance, validated_data):
        print(validated_data)
        instance.name = validated_data.get("name", instance.name)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longtitude = validated_data.get("longtitude", instance.longtitude)
        instance.price_per_hour = validated_data.get("price_per_hour", instance.price_per_hour)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.save()
        return instance