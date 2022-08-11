from hashlib import new
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import string
import random


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username']
            ),
        ]
    
    def validate_username(self, username):
        print(username)
        if username == 'me':
            raise serializers.ValidationError(
                "Нельзя использовать 'me' в качестве имени пользователя"
            )
        return username
    
    def create(self, validated_data):
        new_password = ''.join(random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 12
            )
        )
        validated_data['password'] = new_password

        new_user_email = self.validated_data['email']
        new_user_username = self.validated_data['username']
        new_password = self.validated_data['password']
        user = User.objects.create_user(
            username=new_user_username,
            email=new_user_email
        )
        
        user.set_password(make_password(new_password))
        user.save()
        send_mail(
            'Подтверждение регистрации',
            f'Ваш код получения токена авторизации: {new_password}',
            f'admin@{settings.ADMIN_EMAIL}',
            new_user_email
        )
        return user


class TokenSerializer(TokenObtainPairSerializer):
    pass