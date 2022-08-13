from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        blank=True,
        null=True
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        verbose_name='Биография',
        max_length=1024,
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=5,
        verbose_name='Код подтверждения',
        blank=True
    )
