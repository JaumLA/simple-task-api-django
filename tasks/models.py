from datetime import date, datetime, timedelta

from django.db import models
from django.utils import timezone
from django.conf import settings

class Task(models.Model):
  class TaskStatus(models.TextChoices):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

  description = models.CharField(max_length=200)
  init_time = models.TimeField(verbose_name="Init time")
  end_time = models.TimeField(verbose_name="End time")
  status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.PENDING)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks', default=None)
  
  @property
  def remaining_time(self) -> timedelta | None:
    time_now = timezone.localtime().time()
    date_now = date.today()
    dt_now = datetime.combine(date_now, time_now)
    dt_fim = datetime.combine(date_now, self.end_time)
    if self.status == self.TaskStatus.IN_PROGRESS:
      return dt_fim - dt_now
    elif self.status == self.TaskStatus.PENDING:
      return timedelta(0)

  def __str__(self) -> str:
    return self.description