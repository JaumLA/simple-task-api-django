from rest_framework import serializers

from tasks.models import Task
from .models import User

class UserSerializer(serializers.ModelSerializer):
  tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

  class Meta:
    model = User
    fields = ["id", "username", "tasks"]