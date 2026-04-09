from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
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
			"status"
		)

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

		user = self.context['request'].user

		# Check if a task is over another task's time
		filtered_tasks = Task.objects.filter(
			user=user,
			init_time__lt=attrs['end_time'],
			end_time__gt=attrs['init_time']
		)
		if self.instance:
			filtered_tasks = filtered_tasks.exclude(id=self.instance.id)

		if filtered_tasks.exists():
			raise serializers.ValidationError("Task overlaps with another task.")

		return attrs
