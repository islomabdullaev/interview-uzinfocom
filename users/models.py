from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BaseModel
from users.choices import UserRoleType


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):

        user = self.model(phone_number=phone_number, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=80, null=True, blank=True)
    username = models.CharField(max_length=45)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=13, choices=UserRoleType.choices,
        default=UserRoleType.client.value)
    
    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class UserLocation(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="location")
    longtitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user.username} - {self.country} - {self.city}"
