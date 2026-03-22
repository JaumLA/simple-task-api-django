from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

from tasks.models import Task

class UserSerializer(serializers.ModelSerializer):
  tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

  class Meta:
    model = AbstractUser
    fields = ["id", "username", "tasks"]