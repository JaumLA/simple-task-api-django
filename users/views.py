from django.contrib.auth.models import AbstractUser
from rest_framework import generics

from users.serializers import UserSerializer

class UserList(generics.ListAPIView):
  queryset = AbstractUser.objects.all()
  serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
  queryset = AbstractUser.objects.all()
  serializer_class = UserSerializer