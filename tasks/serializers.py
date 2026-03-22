from rest_framework import serializers
from django.utils import timezone
from datetime import datetime

from .models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    status = serializers.ReadOnlyField()
    remaining_time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'url',
            'id',
            'description',
            'init_time',
            'end_time',
            'remaining_time',
            "status",
            'user'
        )
        extra_kwargs = {
            'url': {'view_name': 'detail', 'lookup_field': 'pk'}
        }

    def get_remaining_time(self, obj):
        delta = obj.remaining_time
        if delta is None or delta.total_seconds() < 0:
            return '00:00:00'
        
        total_segundos = int(delta.total_seconds())
        horas, resto = divmod(total_segundos, 3600)
        minutos, segundos = divmod(resto, 60)

        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def validate(self, attrs):
        if attrs['end_time'] < attrs['init_time']:
            raise serializers.ValidationError("End time must be greater than init time.")
        # Keep TimeField values as times here; convert to datetimes when saving.
        return attrs