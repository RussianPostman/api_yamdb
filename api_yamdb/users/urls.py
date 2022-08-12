from django.urls import path, include
from rest_framework import routers
from .views import create_user, UserViewSet, create_token


router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('auth/signup/', create_user),
    path('auth/token/', create_token),
    path('', include(router_v1.urls)),
]
