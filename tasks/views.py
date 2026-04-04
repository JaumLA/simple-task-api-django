from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from .permissions import IsOwner

class TaskViewSet(ModelViewSet):
  queryset = Task.objects.order_by("init_time").prefetch_related('user')
  serializer_class = TaskSerializer
  permission_classes = [permissions.IsAuthenticated, IsOwner]

  filterset_class = TaskFilter

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  @action(detail=True, methods=['patch'])
  def finish_early(self, request, pk=None):
    pass