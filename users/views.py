from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Prefetch

from users.serializers import UserSerializer, RegisterSerializer
from users.models import User
from tasks.models import Task

class UserViewSet(ModelViewSet):
  queryset = User.objects.all().prefetch_related(
    Prefetch('tasks', queryset=Task.objects.order_by('init_time'))
  )
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

class RegisterCreateAPIView(CreateAPIView):
  queryset = User.objects.all()
  permission_classes = [AllowAny]
  serializer_class = RegisterSerializer
