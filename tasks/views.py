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
    queryset = Task.objects.order_by("init_time").prefetch_related("user")
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filterset_class = TaskFilter

    # helper functions
    def _get_current_task(self, user):
        time_now = timezone.localtime().time()
        task = self.get_queryset().filter(
            user=user, init_time__lte=time_now, end_time__gte=time_now
        )
        print(task)
        return task.first()

    def _start_specific_task(self, task):
        task.status = Task.TaskStatus.IN_PROGRESS
        task.save()

        return task

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def start_day(self, request):
        time_now = timezone.localtime().time()
        task = self._get_current_task(request.user)
        if task is not None:
            _ = self._start_specific_task(task)

        finished_tasks = self.get_queryset().filter(
            user=request.user, end_time__lte=time_now
        )
        finished_tasks.update(status=Task.TaskStatus.COMPLETED)

        pending_tasks = self.get_queryset().filter(
            user=request.user, init_time__gt=time_now
        )
        pending_tasks.update(status=Task.TaskStatus.PENDING)
        user_tasks = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(user_tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def finish_early(self, request, pk=None):
        task = self.get_object()
        time_now = timezone.localtime()

        if (
            task.status == Task.TaskStatus.IN_PROGRESS
            and task.init_time < time_now.time()
        ):
            task.status = Task.TaskStatus.COMPLETED
            task.end_time = time_now.replace(second=0, microsecond=0).time()
            task.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def start_task(self, request, pk=None):
        task = self.get_object()
        time_now = timezone.localtime()

        if task.end_time > time_now.time():
            task = self._start_specific_task(task)
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def current_tasks(self, request):
        tasks = self._get_current_task(request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
