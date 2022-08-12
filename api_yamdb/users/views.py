from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from string import digits
import random


User = get_user_model()


@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    confirmation_code = ''.join(random.choices(digits, k=5))
    serializer.save(confirmation_code=confirmation_code)

    send_mail(
        subject='Registration from YaMDB',
        message=f'Your confirmation code is {confirmation_code}',
        from_email=settings.ADMIN_EMAIL,
        recipient_list=(request.data['email'],))

    return Response(
        serializer.data
    )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


@api_view(['POST'])
def create_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    if not username or not confirmation_code:
        return Response('Одно или несколько обязательных полей пропущены', status=status.HTTP_400_BAD_REQUEST)
    
    if not User.objects.filter(username=username).exists():
        return Response('Имя пользователя неверное', status=status.HTTP_404_NOT_FOUND)
    
    user = User.objects.get(username=username)
    

    if user.confirmation_code == confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {
        
        'access': str(token)
    }
        )

    return Response('Код подтверждения неверен', status=status.HTTP_400_BAD_REQUEST)
