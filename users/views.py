from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from users.serializers import UserSerializer
from users.models import User
from tasks.models import Task

class UserViewSet(ModelViewSet):
  queryset = User.objects.all().prefetch_related(
    Prefetch('tasks', queryset=Task.objects.order_by('init_time'))
  )
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]