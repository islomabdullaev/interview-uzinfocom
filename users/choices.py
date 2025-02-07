from django.db import models

class UserRoleType(models.TextChoices):
    admin = 'admin'
    owner = 'owner'
    client = 'client'
