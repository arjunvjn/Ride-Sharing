from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    class UserRole(models.TextChoices):
        DRIVER = "driver"
        RIDER = "rider"

    name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=UserRole.choices, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def __str__(self):
        return self.username
