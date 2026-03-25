from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer
from users.models import User

class UserViewSet(ModelViewSet):
  queryset = User.objects.all().prefetch_related("tasks")
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    if self.request.user.is_superuser:
      return User.objects.all().prefetch_related("tasks")

    return User.objects.filter(id=self.request.user.id).prefetch_related("tasks")