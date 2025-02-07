from rest_framework import serializers
from rest_framework.validators import ValidationError

from users.choices import UserRoleType

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=13)
    username = serializers.CharField(max_length=24)
    role = serializers.ChoiceField(
        choices=UserRoleType.choices,
        default=UserRoleType.client.value)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "username", "role", "password"]

    def validate(self, attrs):

        phone_number_exists = User.objects.filter(phone_number=attrs["phone_number"]).exists()

        if phone_number_exists:
            raise ValidationError("Phone number has already been used !")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=13)
    password = serializers.CharField(min_length=8, write_only=True)
        
    class Meta:
        model = User
        fields = ["phone_number", "password"]


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "username", "role"]
