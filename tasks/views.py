from django.utils import timezone

from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

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
    task = self.get_object()
    time_now = timezone.localtime()
    
    if task.status == Task.TaskStatus.IN_PROGRESS and task.init_time < time_now.time():
      task.status = Task.TaskStatus.COMPLETED
      task.end_time = time_now.replace(second=0, microsecond=0).time()
      task.save()
      serializer = self.get_serializer(task)
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
  @action(detail=False, methods=['get'])
  def current_tasks(self, request):
    time_now = timezone.localtime().time()
    tasks = self.get_queryset().filter(
      init_time__lte=time_now, end_time__gte=time_now
    )
    serializer = self.get_serializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)