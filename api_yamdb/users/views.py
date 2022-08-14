import random
from string import digits
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .models import User
from .permissions import AdminAndSuperuserOnly
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.serializers import SlugRelatedField


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
    permission_classes = (AdminAndSuperuserOnly,)
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    
    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[IsAuthenticated, ]
    )
    def me_profile(self, request, pk=None):
        username = request.user.username
        user = User.objects.get(username=username)
        if request.method == 'PATCH':
            serializer=UserSerializer(user, data=request.data, partial=True, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                print(serializer.errors)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def create_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    if not username or not confirmation_code:
        return Response(
            'Одно или несколько обязательных полей пропущены',
            status=status.HTTP_400_BAD_REQUEST
        )

    if not User.objects.filter(username=username).exists():
        return Response(
            'Имя пользователя неверное',
            status=status.HTTP_404_NOT_FOUND
        )

    user = User.objects.get(username=username)

    if user.confirmation_code == confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {
                'access': str(token)
            }
        )

    return Response(
        'Код подтверждения неверен',
        status=status.HTTP_400_BAD_REQUEST
    )
