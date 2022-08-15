from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, create_token, create_user

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('auth/signup/', create_user),
    path('auth/token/', create_token),
    path('', include(router_v1.urls)),
]
