from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, create_token, create_user

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', create_user),
    path('v1/auth/token/', create_token),
    path('v1/', include(router_v1.urls)),
]
