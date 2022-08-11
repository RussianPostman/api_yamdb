from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        (1, 'user'),
        (2, 'moderator'),
        (3, 'admin'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )
    email = models.EmailField(max_length=254, unique=True)
