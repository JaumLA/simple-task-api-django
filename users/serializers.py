from rest_framework import serializers

from tasks.models import Task
from tasks.serializers import TaskSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
  tasks = TaskSerializer(many=True)
  class Meta:
    model = User
    fields = ["id", "username", "tasks"]