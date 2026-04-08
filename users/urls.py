from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterCreateAPIView

router = DefaultRouter()

router.register(r'users', UserViewSet, basename="user")

urlpatterns = [
  path("users/register/", RegisterCreateAPIView.as_view(), name="register-user"),
  path("", include(router.urls)),
]