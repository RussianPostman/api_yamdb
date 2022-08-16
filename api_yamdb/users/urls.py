from django.urls import path, include
from rest_framework import routers
from .views import create_user, UserViewSet, create_token


router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', create_user),
    path('v1/auth/token/', create_token),
    path('v1/', include(router_v1.urls)),
]
