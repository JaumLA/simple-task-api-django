from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Task

class UserSerializer(serializers.ModelSerializer):
  tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

  class Meta:
    model = User
    fields = ["id", "username", "tasks"]