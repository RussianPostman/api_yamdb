from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import CreateUserView


# router = routers.DefaultRouter()
# router.register(r'auth/signup/', CreateUserView)

urlpatterns = [
    path('auth/signup/', CreateUserView)
    # path('', include(router.urls))
]
