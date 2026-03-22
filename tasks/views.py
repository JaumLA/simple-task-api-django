from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import renderers

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner

class TaskHighlight(generics.ListAPIView):
  queryset = Task.objects.order_by("init_time")
  renderer_classes = [renderers.StaticHTMLRenderer]

  def get(self, request, *arg, **kwargs):
    task = self.get_object()
    return Response(task.highlighted)

class TaskList(generics.ListCreateAPIView):
  queryset = Task.objects.order_by("init_time")
  serializer_class = TaskSerializer
  permission_classes = [permissions.IsAuthenticated, IsOwner]

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def get_queryset(self):
    user = self.request.user
    return Task.objects.filter(user=user).order_by("init_time")

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  permission_classes = [permissions.IsAuthenticated, IsOwner]
