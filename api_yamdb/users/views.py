from .models import User
from .serializers import UserSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


class CreateUserView(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny, )
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
