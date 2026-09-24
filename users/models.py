from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_DRIVER = "driver"
    ROLE_RIDER = "rider"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_DRIVER, "Driver"),
        (ROLE_RIDER, "Rider"),
    ]

    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default=ROLE_RIDER)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
